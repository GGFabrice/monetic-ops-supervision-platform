CREATE TABLE IF NOT EXISTS monetic.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    week_of_year INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS monetic.dim_bank (
    bank_key SERIAL PRIMARY KEY,
    bank_code VARCHAR(20) NOT NULL UNIQUE,
    bank_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) DEFAULT 'Côte d''Ivoire',
    status VARCHAR(20) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS monetic.dim_customer (
    customer_key BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    customer_type VARCHAR(30),
    gender VARCHAR(10),
    age INTEGER,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Côte d''Ivoire',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monetic.dim_card (
    card_key BIGSERIAL PRIMARY KEY,
    card_id VARCHAR(50) NOT NULL UNIQUE,
    card_type VARCHAR(30),
    card_network VARCHAR(30),
    card_status VARCHAR(20),
    customer_key BIGINT REFERENCES monetic.dim_customer(customer_key),
    bank_key INTEGER REFERENCES monetic.dim_bank(bank_key)
);

CREATE TABLE IF NOT EXISTS monetic.dim_terminal (
    terminal_key SERIAL PRIMARY KEY,
    terminal_id VARCHAR(50) NOT NULL UNIQUE,
    terminal_type VARCHAR(20) NOT NULL,
    terminal_status VARCHAR(20),
    bank_key INTEGER REFERENCES monetic.dim_bank(bank_key),
    city VARCHAR(100),
    location VARCHAR(200),
    installation_date DATE
);

CREATE TABLE IF NOT EXISTS monetic.dim_merchant (
    merchant_key SERIAL PRIMARY KEY,
    merchant_id VARCHAR(50) NOT NULL UNIQUE,
    merchant_name VARCHAR(150) NOT NULL,
    merchant_category VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Côte d''Ivoire',
    status VARCHAR(20) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS monetic.dim_location (
    location_key SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Côte d''Ivoire'
);

CREATE TABLE IF NOT EXISTS monetic.dim_transaction_type (
    transaction_type_key SERIAL PRIMARY KEY,
    transaction_code VARCHAR(20) NOT NULL UNIQUE,
    transaction_name VARCHAR(100) NOT NULL,
    channel VARCHAR(30),
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS monetic.dim_response_code (
    response_code_key SERIAL PRIMARY KEY,
    response_code VARCHAR(10) NOT NULL UNIQUE,
    response_label VARCHAR(100) NOT NULL,
    response_category VARCHAR(50),
    is_success BOOLEAN NOT NULL DEFAULT FALSE
);