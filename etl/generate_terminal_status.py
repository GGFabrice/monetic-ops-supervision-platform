import random
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "monetic_dw",
    "user": "monetic_user",
    "password": "monetic_password",
}

BATCH_SIZE = 5000
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_terminals(cursor):
    cursor.execute("""
        SELECT
            terminal_key,
            terminal_type
        FROM monetic.dim_terminal
        ORDER BY terminal_key;
    """)

    return cursor.fetchall()


def load_dates(cursor):
    cursor.execute("""
        SELECT
            date_key,
            full_date
        FROM monetic.dim_date
        ORDER BY full_date;
    """)

    return cursor.fetchall()


def generate_status():
    statuses = [
        "ONLINE",
        "DEGRADED",
        "OFFLINE",
        "MAINTENANCE"
    ]

    weights = [
        0.88,
        0.06,
        0.04,
        0.02
    ]

    return random.choices(
        statuses,
        weights=weights,
        k=1
    )[0]


def generate_response_time(status):
    if status == "ONLINE":
        return random.randint(150, 800)

    if status == "DEGRADED":
        return random.randint(800, 3000)

    return None


def generate_terminal_status():
    connection = get_connection()
    cursor = connection.cursor()

    print("Chargement des terminaux...")
    terminals = load_terminals(cursor)

    print("Chargement des dates...")
    dates = load_dates(cursor)

    print(f"Terminaux chargés : {len(terminals)}")
    print(f"Dates chargées : {len(dates)}")

    total_expected = len(terminals) * len(dates) * 8

    print(f"Volume attendu : {total_expected:,} observations")
    print()

    insert_query = """
        INSERT INTO monetic.fact_terminal_status
        (
            terminal_key,
            date_key,
            status_timestamp,
            status,
            response_time_ms,
            uptime_percentage,
            incident_flag
        )
        VALUES %s
    """

    batch = []
    total_inserted = 0

    observation_hours = [
        0,
        3,
        6,
        9,
        12,
        15,
        18,
        21
    ]

    for terminal_key, terminal_type in terminals:

        for date_key, full_date in dates:

            daily_rows = []
            daily_statuses = []

            for hour in observation_hours:

                status = generate_status()

                response_time = generate_response_time(status)

                status_timestamp = (
                    datetime.combine(
                        full_date,
                        datetime.min.time()
                    )
                    + timedelta(hours=hour)
                )

                incident_flag = status in (
                    "DEGRADED",
                    "OFFLINE"
                )

                daily_statuses.append(status)

                daily_rows.append(
                    (
                        terminal_key,
                        date_key,
                        status_timestamp,
                        status,
                        response_time,
                        None,
                        incident_flag
                    )
                )

            available_count = sum(
                status in (
                    "ONLINE",
                    "DEGRADED"
                )
                for status in daily_statuses
            )

            uptime_percentage = round(
                available_count / len(daily_statuses) * 100,
                2
            )

            daily_rows = [
                (
                    terminal_key,
                    date_key,
                    status_timestamp,
                    status,
                    response_time,
                    uptime_percentage,
                    incident_flag
                )
                for (
                    terminal_key,
                    date_key,
                    status_timestamp,
                    status,
                    response_time,
                    _,
                    incident_flag
                ) in daily_rows
            ]

            batch.extend(daily_rows)

            if len(batch) >= BATCH_SIZE:

                execute_values(
                    cursor,
                    insert_query,
                    batch
                )

                connection.commit()

                total_inserted += len(batch)

                print(
                    f"Observations insérées : "
                    f"{total_inserted:,}/{total_expected:,}"
                )

                batch.clear()

    if batch:

        execute_values(
            cursor,
            insert_query,
            batch
        )

        connection.commit()

        total_inserted += len(batch)

    cursor.close()
    connection.close()

    print()
    print("========================================")
    print("GENERATION TERMINÉE")
    print("========================================")
    print(f"Total inséré  : {total_inserted:,}")
    print(f"Total attendu : {total_expected:,}")


if __name__ == "__main__":
    generate_terminal_status()