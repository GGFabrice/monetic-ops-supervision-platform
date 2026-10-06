import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "monetic_dw",
    "user": "monetic_user",
    "password": "monetic_password",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_one(query):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def test_transactions_count():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fact_transactions;
    """)
    assert result == 100000


def test_fraud_alerts_count():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fraud_alerts;
    """)
    assert result == 100000


def test_transactions_without_location():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fact_transactions
        WHERE location_key IS NULL;
    """)
    assert result == 0


def test_duplicate_transaction_ids():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM (
            SELECT transaction_id
            FROM monetic.fact_transactions
            GROUP BY transaction_id
            HAVING COUNT(*) > 1
        ) duplicates;
    """)
    assert result == 0


def test_invalid_risk_scores():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fraud_alerts
        WHERE risk_score < 0
           OR risk_score > 100;
    """)
    assert result == 0


def test_invalid_risk_levels():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fraud_alerts
        WHERE risk_level NOT IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
    """)
    assert result == 0


def test_orphan_alerts():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fraud_alerts fa
        LEFT JOIN monetic.fact_transactions ft
            ON fa.transaction_key = ft.transaction_key
        WHERE ft.transaction_key IS NULL;
    """)
    assert result == 0


def test_success_response_code_consistency():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fact_transactions ft
        JOIN monetic.dim_response_code rc
            ON ft.response_code_key = rc.response_code_key
        WHERE ft.is_success <> rc.is_success;
    """)
    assert result == 0


def test_alert_amount_consistency():
    result = fetch_one("""
        SELECT COUNT(*)
        FROM monetic.fraud_alerts fa
        JOIN monetic.fact_transactions ft
            ON fa.transaction_key = ft.transaction_key
        WHERE fa.transaction_amount <> ft.amount;
    """)
    assert result == 0