import random
from datetime import timedelta

import psycopg2
from psycopg2.extras import execute_values


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "monetic_dw",
    "user": "monetic_user",
    "password": "monetic_password",
}

BATCH_SIZE = 2000
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_terminal_status(cursor):
    cursor.execute("""
        SELECT
            fts.terminal_key,
            dt.bank_key,
            fts.date_key,
            fts.status_timestamp,
            fts.status,
            fts.response_time_ms
        FROM monetic.fact_terminal_status fts
        JOIN monetic.dim_terminal dt
            ON dt.terminal_key = fts.terminal_key
        ORDER BY
            fts.terminal_key,
            fts.status_timestamp;
    """)

    return cursor


def is_problematic(status):
    return status in (
        "DEGRADED",
        "OFFLINE"
    )


def build_incident(run, incident_number):
    statuses = [row[4] for row in run]

    has_offline = "OFFLINE" in statuses

    if has_offline:
        if len(run) >= 2:
            severity = "CRITICAL"
        else:
            severity = "HIGH"

        incident_type = random.choice([
            "CONNECTIVITY",
            "SYSTEM_FAILURE"
        ])

        description = (
            "Indisponibilité du terminal détectée "
            "par le système de supervision"
        )

    else:
        if len(run) >= 3:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        incident_type = "PERFORMANCE"

        description = (
            "Dégradation des performances du terminal "
            "détectée par le système de supervision"
        )

    incident_timestamp = run[0][3]
    terminal_key = run[0][0]
    bank_key = run[0][1]
    date_key = run[0][2]

    base_duration = len(run) * 180

    if severity == "MEDIUM":
        additional_duration = random.randint(30, 120)

    elif severity == "HIGH":
        additional_duration = random.randint(60, 240)

    else:
        additional_duration = random.randint(120, 480)

    resolution_time_minutes = max(
        base_duration,
        additional_duration
    )

    status_roll = random.random()

    if status_roll < 0.92:
        incident_status = "RESOLVED"

        resolved_at = (
            incident_timestamp
            + timedelta(minutes=resolution_time_minutes)
        )

    elif status_roll < 0.97:
        incident_status = "IN_PROGRESS"
        resolution_time_minutes = None
        resolved_at = None

    else:
        incident_status = "OPEN"
        resolution_time_minutes = None
        resolved_at = None

    incident_id = f"INC{incident_number:06d}"

    return (
        incident_id,
        terminal_key,
        bank_key,
        date_key,
        incident_timestamp,
        incident_type,
        severity,
        description,
        incident_status,
        resolution_time_minutes,
        resolved_at
    )


def generate_incidents():
    read_connection = get_connection()
    write_connection = get_connection()

    read_cursor = read_connection.cursor(
        name="terminal_status_cursor"
    )

    write_cursor = write_connection.cursor()

    print("Chargement des observations de supervision...")

    status_cursor = load_terminal_status(read_cursor)
    status_cursor.itersize = 10000

    insert_query = """
        INSERT INTO monetic.fact_incidents
        (
            incident_id,
            terminal_key,
            bank_key,
            date_key,
            incident_timestamp,
            incident_type,
            severity,
            description,
            status,
            resolution_time_minutes,
            resolved_at
        )
        VALUES %s
    """

    batch = []

    total_incidents = 0
    total_runs = 0

    current_run = []

    previous_terminal_key = None
    previous_timestamp = None

    def finalize_run(run):
        nonlocal total_incidents
        nonlocal total_runs

        if not run:
            return

        total_runs += 1

        statuses = [row[4] for row in run]

        if "OFFLINE" in statuses:
            selection_probability = 0.30
        else:
            selection_probability = 0.20

        if random.random() > selection_probability:
            return

        total_incidents += 1

        incident = build_incident(
            run,
            total_incidents
        )

        batch.append(incident)

        if len(batch) >= BATCH_SIZE:
            execute_values(
                write_cursor,
                insert_query,
                batch
            )

            write_connection.commit()

            print(
                f"Incidents générés : "
                f"{total_incidents:,}"
            )

            batch.clear()

    try:

        for row in status_cursor:

            terminal_key = row[0]
            status_timestamp = row[3]
            status = row[4]

            problematic = is_problematic(status)

            is_continuous = (
                current_run
                and terminal_key == previous_terminal_key
                and previous_timestamp is not None
                and status_timestamp - previous_timestamp
                == timedelta(hours=3)
                and problematic
            )

            if problematic:

                if is_continuous:
                    current_run.append(row)

                else:
                    finalize_run(current_run)
                    current_run = [row]

            else:
                finalize_run(current_run)
                current_run = []

            previous_terminal_key = terminal_key
            previous_timestamp = status_timestamp

        finalize_run(current_run)

        if batch:
            execute_values(
                write_cursor,
                insert_query,
                batch
            )

            write_connection.commit()

            batch.clear()

    except Exception:
        write_connection.rollback()
        raise

    finally:
        try:
            read_cursor.close()
        except Exception:
            pass

        try:
            write_cursor.close()
        except Exception:
            pass

        read_connection.close()
        write_connection.close()

    print()
    print("========================================")
    print("GÉNÉRATION DES INCIDENTS TERMINÉE")
    print("========================================")
    print(
        f"Groupes d'anomalies analysés : "
        f"{total_runs:,}"
    )
    print(
        f"Incidents générés             : "
        f"{total_incidents:,}"
    )


if __name__ == "__main__":
    generate_incidents()