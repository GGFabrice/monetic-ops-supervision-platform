import random
from datetime import date, timedelta

import psycopg2
from faker import Faker


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "monetic_dw",
    "user": "monetic_user",
    "password": "monetic_password",
}

NB_CUSTOMERS = 500
NB_CARDS = 500
NB_TERMINALS = 200
NB_MERCHANTS = 300

fake = Faker("fr_FR")

random.seed(42)
Faker.seed(42)


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def generate_customers(cursor):
    cities = [
        "Abidjan",
        "Bouaké",
        "Yamoussoukro",
        "San-Pédro",
        "Korhogo",
        "Daloa",
    ]

    customer_types = [
        "INDIVIDUAL",
        "PREMIUM",
        "BUSINESS",
    ]

    genders = ["M", "F"]

    for i in range(1, NB_CUSTOMERS + 1):
        customer_id = f"CUST{i:05d}"
        customer_type = random.choice(customer_types)
        gender = random.choice(genders)
        age = random.randint(18, 70)
        city = random.choice(cities)

        cursor.execute(
            """
            INSERT INTO monetic.dim_customer
            (
                customer_id,
                customer_type,
                gender,
                age,
                city
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING;
            """,
            (
                customer_id,
                customer_type,
                gender,
                age,
                city,
            ),
        )


def generate_cards(cursor):
    cursor.execute(
        """
        SELECT customer_key, customer_id
        FROM monetic.dim_customer
        ORDER BY customer_key;
        """
    )

    customers = cursor.fetchall()

    cursor.execute(
        """
        SELECT bank_key
        FROM monetic.dim_bank
        ORDER BY bank_key;
        """
    )

    banks = [row[0] for row in cursor.fetchall()]

    card_types = [
        "DEBIT",
        "CREDIT",
        "PREPAID",
    ]

    card_networks = [
        "VISA",
        "MASTERCARD",
    ]

    card_statuses = [
        "ACTIVE",
        "ACTIVE",
        "ACTIVE",
        "BLOCKED",
    ]

    for i, (customer_key, customer_id) in enumerate(
        customers[:NB_CARDS],
        start=1,
    ):
        card_id = f"CARD{i:06d}"
        card_type = random.choice(card_types)
        card_network = random.choice(card_networks)
        card_status = random.choice(card_statuses)
        bank_key = random.choice(banks)

        cursor.execute(
            """
            INSERT INTO monetic.dim_card
            (
                card_id,
                card_type,
                card_network,
                card_status,
                customer_key,
                bank_key
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (card_id) DO NOTHING;
            """,
            (
                card_id,
                card_type,
                card_network,
                card_status,
                customer_key,
                bank_key,
            ),
        )


def generate_terminals(cursor):
    cursor.execute(
        """
        SELECT bank_key
        FROM monetic.dim_bank
        ORDER BY bank_key;
        """
    )

    banks = [row[0] for row in cursor.fetchall()]

    cities = [
        "Abidjan",
        "Bouaké",
        "Yamoussoukro",
        "San-Pédro",
        "Korhogo",
        "Daloa",
    ]

    statuses = [
        "ONLINE",
        "ONLINE",
        "ONLINE",
        "ONLINE",
        "OFFLINE",
        "MAINTENANCE",
    ]

    for i in range(1, NB_TERMINALS + 1):
        if i <= 120:
            terminal_type = "ATM"
        else:
            terminal_type = "POS"

        terminal_id = f"TERM{i:04d}"
        terminal_status = random.choice(statuses)
        bank_key = random.choice(banks)
        city = random.choice(cities)

        cursor.execute(
            """
            INSERT INTO monetic.dim_terminal
            (
                terminal_id,
                terminal_type,
                terminal_status,
                bank_key,
                city,
                location,
                installation_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (terminal_id) DO NOTHING;
            """,
            (
                terminal_id,
                terminal_type,
                terminal_status,
                bank_key,
                city,
                f"Zone {random.randint(1, 20)}",
                date.today()
                - timedelta(days=random.randint(30, 1000)),
            ),
        )


def generate_merchants(cursor):
    cities = [
        "Abidjan",
        "Bouaké",
        "Yamoussoukro",
        "San-Pédro",
        "Korhogo",
        "Daloa",
    ]

    merchant_categories = [
        "SUPERMARKET",
        "PHARMACY",
        "FUEL",
        "RESTAURANT",
        "RETAIL",
        "HOTEL",
        "ELECTRONICS",
        "CLOTHING",
        "TRANSPORT",
        "OTHER",
    ]

    merchant_names = [
        "Supermarché",
        "Pharmacie",
        "Station Service",
        "Restaurant",
        "Boutique",
        "Hôtel",
        "Électronique",
        "Mode",
        "Transport",
        "Commerce",
    ]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM monetic.dim_merchant;
        """
    )

    current_count = cursor.fetchone()[0]

    for i in range(current_count + 1, NB_MERCHANTS + 1):
        merchant_id = f"MERCH{i:04d}"

        category_index = (i - 1) % len(merchant_categories)

        merchant_category = merchant_categories[category_index]
        merchant_prefix = merchant_names[category_index]

        city = random.choice(cities)

        merchant_name = (
            f"{merchant_prefix} "
            f"{city} {i:03d}"
        )

        cursor.execute(
            """
            INSERT INTO monetic.dim_merchant
            (
                merchant_id,
                merchant_name,
                merchant_category,
                city,
                country,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (merchant_id) DO NOTHING;
            """,
            (
                merchant_id,
                merchant_name,
                merchant_category,
                city,
                "Côte d'Ivoire",
                "ACTIVE",
            ),
        )


def main():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        print("Génération des clients...")
        generate_customers(cursor)

        print("Génération des cartes...")
        generate_cards(cursor)

        print("Génération des terminaux...")
        generate_terminals(cursor)

        print("Génération des commerçants...")
        generate_merchants(cursor)

        connection.commit()

        print(
            "Clients, cartes, terminaux et commerçants "
            "générés avec succès."
        )

        cursor.close()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()