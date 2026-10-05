import random
from datetime import datetime

import psycopg2
from psycopg2.extras import execute_values


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "monetic_dw",
    "user": "monetic_user",
    "password": "monetic_password",
}

NB_TRANSACTIONS = 100_000
BATCH_SIZE = 5_000

random.seed(42)


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_reference_data(cursor):
    cursor.execute("""
        SELECT
            card_key,
            customer_key,
            bank_key
        FROM monetic.dim_card
        ORDER BY card_key;
    """)
    cards = cursor.fetchall()

    cursor.execute("""
        SELECT
            customer_key,
            city
        FROM monetic.dim_customer;
    """)
    customers = cursor.fetchall()

    cursor.execute("""
        SELECT
            terminal_key,
            terminal_type,
            bank_key,
            city
        FROM monetic.dim_terminal
        ORDER BY terminal_key;
    """)
    terminals = cursor.fetchall()

    cursor.execute("""
        SELECT
            merchant_key,
            city
        FROM monetic.dim_merchant
        ORDER BY merchant_key;
    """)
    merchants = cursor.fetchall()

    cursor.execute("""
        SELECT
            transaction_type_key,
            transaction_code,
            channel
        FROM monetic.dim_transaction_type
        ORDER BY transaction_type_key;
    """)
    transaction_types = cursor.fetchall()

    cursor.execute("""
        SELECT
            response_code_key,
            response_code,
            is_success
        FROM monetic.dim_response_code
        ORDER BY response_code_key;
    """)
    response_codes = cursor.fetchall()

    cursor.execute("""
        SELECT
            date_key,
            full_date
        FROM monetic.dim_date
        ORDER BY full_date;
    """)
    dates = cursor.fetchall()

    cursor.execute("""
        SELECT
            location_key,
            city
        FROM monetic.dim_location;
    """)
    locations = cursor.fetchall()

    return (
        cards,
        customers,
        terminals,
        merchants,
        transaction_types,
        response_codes,
        dates,
        locations,
    )


def build_reference_maps(
    cards,
    customers,
    terminals,
    merchants,
    transaction_types,
    response_codes,
    locations,
):
    customers_by_key = {
        row[0]: row
        for row in customers
    }

    merchants_by_key = {
        row[0]: row
        for row in merchants
    }

    atm_terminals = [
        row
        for row in terminals
        if row[1] == "ATM"
    ]

    pos_terminals = [
        row
        for row in terminals
        if row[1] == "POS"
    ]

    transaction_type_map = {
        row[1]: row
        for row in transaction_types
    }

    response_code_map = {
        row[1]: row
        for row in response_codes
    }

    locations_by_city = {}

    for location_key, city in locations:
        locations_by_city[city] = location_key

    return (
        customers_by_key,
        merchants_by_key,
        atm_terminals,
        pos_terminals,
        transaction_type_map,
        response_code_map,
        locations_by_city,
    )


def choose_transaction_type():
    choices = [
        ("ATM_WD", 0.40),
        ("POS_PAY", 0.35),
        ("TRANSFER", 0.08),
        ("BAL_INQ", 0.07),
        ("CASH_DEP", 0.05),
        ("ONLINE_PAY", 0.05),
    ]

    value = random.random()
    cumulative = 0

    for transaction_code, probability in choices:
        cumulative += probability

        if value <= cumulative:
            return transaction_code

    return "ATM_WD"


def choose_response_code():
    choices = [
        ("00", 0.88),
        ("05", 0.035),
        ("51", 0.025),
        ("14", 0.012),
        ("54", 0.010),
        ("55", 0.008),
        ("57", 0.010),
        ("91", 0.012),
        ("96", 0.008),
    ]

    value = random.random()
    cumulative = 0

    for response_code, probability in choices:
        cumulative += probability

        if value <= cumulative:
            return response_code

    return "00"


def generate_amount(transaction_code):
    if transaction_code == "BAL_INQ":
        return 0.00

    if transaction_code == "ATM_WD":
        amounts = [
            5000,
            10000,
            20000,
            30000,
            40000,
            50000,
            75000,
            100000,
            150000,
            200000,
        ]
        return float(random.choice(amounts))

    if transaction_code == "CASH_DEP":
        return round(random.uniform(10000, 500000), 2)

    if transaction_code == "POS_PAY":
        return round(random.uniform(1000, 250000), 2)

    if transaction_code == "ONLINE_PAY":
        return round(random.uniform(2000, 500000), 2)

    if transaction_code == "TRANSFER":
        return round(random.uniform(5000, 1000000), 2)

    return round(random.uniform(1000, 100000), 2)


def choose_processing_time(transaction_code):
    if transaction_code in (
        "ATM_WD",
        "BAL_INQ",
        "CASH_DEP",
    ):
        return random.randint(400, 4500)

    if transaction_code == "POS_PAY":
        return random.randint(200, 3000)

    if transaction_code == "ONLINE_PAY":
        return random.randint(150, 2500)

    if transaction_code == "TRANSFER":
        return random.randint(500, 5000)

    return random.randint(200, 3000)


def generate_transaction_timestamp(full_date):
    hour = random.choices(
        population=list(range(24)),
        weights=[
            1, 1, 1, 1, 1, 2,
            3, 5, 7, 8, 8, 7,
            7, 7, 7, 7, 8, 9,
            9, 8, 6, 5, 3, 2,
        ],
        k=1,
    )[0]

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return datetime(
        full_date.year,
        full_date.month,
        full_date.day,
        hour,
        minute,
        second,
    )


def choose_terminal(
    transaction_code,
    atm_terminals,
    pos_terminals,
):
    if transaction_code in (
        "ATM_WD",
        "BAL_INQ",
        "CASH_DEP",
    ):
        return random.choice(atm_terminals)

    if transaction_code == "POS_PAY":
        return random.choice(pos_terminals)

    return None


def calculate_suspicious(
    amount,
    transaction_code,
    transaction_timestamp,
    response_code,
    processing_time_ms,
):
    score = 0

    if amount >= 500_000:
        score += 2

    if amount >= 800_000:
        score += 2

    if transaction_timestamp.hour in (
        0, 1, 2, 3, 4, 5
    ):
        score += 2

    if (
        transaction_code == "TRANSFER"
        and amount >= 500_000
    ):
        score += 2

    if (
        transaction_code == "ONLINE_PAY"
        and amount >= 300_000
    ):
        score += 2

    if response_code in ("91", "96"):
        score += 1

    if processing_time_ms >= 4000:
        score += 1

    return score >= 3


def get_location_key(
    transaction_code,
    terminal,
    merchant_key,
    customer_key,
    customers_by_key,
    merchants_by_key,
    locations_by_city,
):
    if terminal is not None:
        city = terminal[3]
    elif transaction_code == "ONLINE_PAY":
        city = merchants_by_key[merchant_key][1]
    else:
        city = customers_by_key[customer_key][1]

    return locations_by_city.get(city)


def generate_transactions():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        print("Chargement des données de référence...")

        (
            cards,
            customers,
            terminals,
            merchants,
            transaction_types,
            response_codes,
            dates,
            locations,
        ) = load_reference_data(cursor)

        (
            customers_by_key,
            merchants_by_key,
            atm_terminals,
            pos_terminals,
            transaction_type_map,
            response_code_map,
            locations_by_city,
        ) = build_reference_maps(
            cards,
            customers,
            terminals,
            merchants,
            transaction_types,
            response_codes,
            locations,
        )

        print(f"Cartes disponibles     : {len(cards)}")
        print(f"Clients disponibles    : {len(customers)}")
        print(f"Terminaux disponibles  : {len(terminals)}")
        print(f"Terminaux ATM          : {len(atm_terminals)}")
        print(f"Terminaux POS          : {len(pos_terminals)}")
        print(f"Commerçants disponibles: {len(merchants)}")
        print(f"Dates disponibles      : {len(dates)}")
        print(f"Localisations          : {len(locations)}")

        if not cards:
            raise Exception("Aucune carte disponible.")

        if not customers:
            raise Exception("Aucun client disponible.")

        if not atm_terminals:
            raise Exception("Aucun terminal ATM disponible.")

        if not pos_terminals:
            raise Exception("Aucun terminal POS disponible.")

        if not merchants:
            raise Exception("Aucun commerçant disponible.")

        if not dates:
            raise Exception("Aucune date disponible.")

        if not locations:
            raise Exception("Aucune localisation disponible.")

        rows = []

        print()
        print(
            f"Génération de {NB_TRANSACTIONS:,} transactions..."
        )

        for i in range(1, NB_TRANSACTIONS + 1):
            card = random.choice(cards)

            card_key = card[0]
            customer_key = card[1]
            bank_key = card[2]

            transaction_code = choose_transaction_type()

            transaction_type = transaction_type_map[
                transaction_code
            ]

            transaction_type_key = transaction_type[0]
            channel = transaction_type[2]

            terminal = choose_terminal(
                transaction_code,
                atm_terminals,
                pos_terminals,
            )

            terminal_key = (
                terminal[0]
                if terminal is not None
                else None
            )

            if transaction_code in (
                "POS_PAY",
                "ONLINE_PAY",
            ):
                merchant_key = random.choice(
                    list(merchants_by_key.keys())
                )
            else:
                merchant_key = None

            date_key, full_date = random.choice(dates)

            transaction_timestamp = (
                generate_transaction_timestamp(full_date)
            )

            response_code = choose_response_code()
            response = response_code_map[response_code]

            response_code_key = response[0]
            is_success = response[2]

            amount = generate_amount(transaction_code)

            processing_time_ms = choose_processing_time(
                transaction_code
            )

            is_suspicious = calculate_suspicious(
                amount,
                transaction_code,
                transaction_timestamp,
                response_code,
                processing_time_ms,
            )

            location_key = get_location_key(
                transaction_code,
                terminal,
                merchant_key,
                customer_key,
                customers_by_key,
                merchants_by_key,
                locations_by_city,
            )

            transaction_id = f"TXN{i:08d}"

            rows.append(
                (
                    transaction_id,
                    date_key,
                    bank_key,
                    customer_key,
                    card_key,
                    terminal_key,
                    merchant_key,
                    location_key,
                    transaction_type_key,
                    response_code_key,
                    transaction_timestamp,
                    amount,
                    "XOF",
                    processing_time_ms,
                    is_success,
                    is_suspicious,
                    channel,
                )
            )

            if len(rows) >= BATCH_SIZE:
                execute_values(
                    cursor,
                    """
                    INSERT INTO monetic.fact_transactions (
                        transaction_id,
                        date_key,
                        bank_key,
                        customer_key,
                        card_key,
                        terminal_key,
                        merchant_key,
                        location_key,
                        transaction_type_key,
                        response_code_key,
                        transaction_timestamp,
                        amount,
                        currency,
                        processing_time_ms,
                        is_success,
                        is_suspicious,
                        channel
                    )
                    VALUES %s
                    """,
                    rows,
                    page_size=BATCH_SIZE,
                )

                connection.commit()

                print(
                    f"Progression : {i:,}/"
                    f"{NB_TRANSACTIONS:,} "
                    f"({i / NB_TRANSACTIONS:.0%})"
                )

                rows = []

        if rows:
            execute_values(
                cursor,
                """
                INSERT INTO monetic.fact_transactions (
                    transaction_id,
                    date_key,
                    bank_key,
                    customer_key,
                    card_key,
                    terminal_key,
                    merchant_key,
                    location_key,
                    transaction_type_key,
                    response_code_key,
                    transaction_timestamp,
                    amount,
                    currency,
                    processing_time_ms,
                    is_success,
                    is_suspicious,
                    channel
                )
                VALUES %s
                """,
                rows,
                page_size=BATCH_SIZE,
            )

            connection.commit()

        cursor.close()

        print()
        print("==========================================")
        print("GENERATION TERMINEE")
        print("==========================================")
        print(
            f"Transactions générées : "
            f"{NB_TRANSACTIONS:,}"
        )

    except Exception as error:
        connection.rollback()
        print()
        print("ERREUR :", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    generate_transactions()