
import os
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, sum, when

DB_URL = "jdbc:postgresql://localhost:5433/monetic_dw"

DB_PROPERTIES = {
    "user": "monetic_user",
    "password": "monetic_password",
    "driver": "org.postgresql.Driver",
}

JDBC_DRIVER = os.path.abspath(
    "spark_jobs/jars/postgresql-42.7.8.jar"
)


def create_spark_session():
    return (
        SparkSession.builder
        .appName("MoneticTransactionAnalysis")
        .master("local[2]")
        .config("spark.driver.extraClassPath", JDBC_DRIVER)
        .getOrCreate()
    )


def load_transactions(spark):
    return spark.read.jdbc(
        url=DB_URL,
        table="monetic.fact_transactions",
        properties=DB_PROPERTIES,
    )


def analyze_transactions(df):
    print("\n=== SCHEMA ===")
    df.printSchema()

    print("\n=== VOLUME ===")
    print(f"Transactions : {df.count():,}")

    print("\n=== KPIs GLOBAUX ===")
    df.agg(
        count("*").alias("total_transactions"),
        sum("amount").alias("total_amount"),
        avg("amount").alias("average_amount"),
        (
            avg(when(df.is_success, 1).otherwise(0)) * 100
        ).alias("success_rate_pct"),
        (
            avg(when(df.is_suspicious, 1).otherwise(0)) * 100
        ).alias("suspicious_rate_pct"),
    ).show(truncate=False)

    print("\n=== TRANSACTIONS PAR CANAL ===")
    (
        df.groupBy("channel")
        .agg(
            count("*").alias("total_transactions"),
            sum("amount").alias("total_amount"),
            avg("amount").alias("average_amount"),
            (
                avg(when(df.is_success, 1).otherwise(0)) * 100
            ).alias("success_rate_pct"),
        )
        .orderBy("total_transactions", ascending=False)
        .show(truncate=False)
    )


def save_channel_kpis(df):
    channel_kpis = (
        df.groupBy("channel")
        .agg(
            count("*").alias("total_transactions"),
            sum("amount").alias("total_amount"),
            avg("amount").alias("average_amount"),
            (
                avg(when(df.is_success, 1).otherwise(0)) * 100
            ).alias("success_rate_pct"),
        )
    )

    rows = channel_kpis.collect()

    with psycopg2.connect(
        host="localhost",
        port=5433,
        dbname="monetic_dw",
        user="monetic_user",
        password="monetic_password",
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM monetic.spark_channel_kpis"
            )

            for row in rows:
                cursor.execute(
                    """
                    INSERT INTO monetic.spark_channel_kpis (
                        channel,
                        total_transactions,
                        total_amount,
                        average_amount,
                        success_rate_pct,
                        analyzed_at
                    )
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """,
                    (
                        row["channel"],
                        row["total_transactions"],
                        row["total_amount"],
                        row["average_amount"],
                        row["success_rate_pct"],
                    ),
                )

    print("\n=== KPI ENREGISTRÉS DANS POSTGRESQL ===")
    channel_kpis.orderBy("channel").show(truncate=False)


def main():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    try:
        transactions = load_transactions(spark)
        analyze_transactions(transactions)
        save_channel_kpis(transactions)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
