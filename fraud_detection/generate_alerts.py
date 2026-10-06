import os
import sys

import psycopg2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fraud_detection.risk_scoring import calculate_risk


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "monetic_dw",
    "user": "monetic_user",
    "password": "monetic_password",
}


def generate_alerts():
    read_conn = psycopg2.connect(**DB_CONFIG)
    write_conn = psycopg2.connect(**DB_CONFIG)

    read_cursor = read_conn.cursor(name="transaction_cursor")
    write_cursor = write_conn.cursor()

    read_cursor.execute("""
        SELECT
            transaction_key,
            transaction_id,
            transaction_timestamp,
            amount,
            processing_time_ms,
            channel,
            bank_key,
            location_key,
            transaction_type_key,
            is_suspicious,
            dr.response_code
        FROM monetic.fact_transactions ft
        JOIN monetic.dim_response_code dr
            ON ft.response_code_key = dr.response_code_key
        ORDER BY transaction_key
    """)

    insert_query = """
        INSERT INTO monetic.fraud_alerts (
            transaction_key,
            transaction_id,
            alert_timestamp,
            risk_score,
            risk_level,
            amount_score,
            unusual_hour_score,
            processing_time_score,
            response_code_score,
            suspicious_flag_score,
            transaction_amount,
            response_code,
            channel,
            bank_key,
            location_key,
            transaction_type_key
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """

    total = 0

    risk_counts = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0,
    }

    try:
        for row in read_cursor:
            (
                transaction_key,
                transaction_id,
                transaction_timestamp,
                amount,
                processing_time_ms,
                channel,
                bank_key,
                location_key,
                transaction_type_key,
                is_suspicious,
                response_code,
            ) = row

            result = calculate_risk(
                amount=float(amount),
                transaction_timestamp=transaction_timestamp,
                processing_time_ms=processing_time_ms,
                response_code=response_code,
                is_suspicious=is_suspicious,
            )

            write_cursor.execute(
                insert_query,
                (
                    transaction_key,
                    transaction_id,
                    transaction_timestamp,
                    result["risk_score"],
                    result["risk_level"],
                    result["amount_score"],
                    result["unusual_hour_score"],
                    result["processing_time_score"],
                    result["response_code_score"],
                    result["suspicious_flag_score"],
                    amount,
                    response_code,
                    channel,
                    bank_key,
                    location_key,
                    transaction_type_key,
                ),
            )

            total += 1
            risk_counts[result["risk_level"]] += 1

            if total % 5000 == 0:
                write_conn.commit()
                print(f"{total:,} transactions analysées")

        write_conn.commit()

    except Exception:
        write_conn.rollback()
        raise

    finally:
        read_cursor.close()
        write_cursor.close()
        read_conn.close()
        write_conn.close()

    print("\n=== RÉSULTAT DU SCORING ===")
    print(f"Transactions analysées : {total:,}")

    for level, count in risk_counts.items():
        percentage = (count / total * 100) if total else 0
        print(f"{level:8} : {count:6,} ({percentage:.2f}%)")


if __name__ == "__main__":
    generate_alerts()