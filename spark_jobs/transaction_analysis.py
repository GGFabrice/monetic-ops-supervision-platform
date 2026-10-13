
import os
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


def main():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    try:
        transactions = load_transactions(spark)
        analyze_transactions(transactions)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
