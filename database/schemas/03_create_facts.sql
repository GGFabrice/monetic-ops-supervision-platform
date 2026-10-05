CREATE TABLE IF NOT EXISTS monetic.fact_transactions (
    transaction_key BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL UNIQUE,
    date_key INTEGER NOT NULL REFERENCES monetic.dim_date(date_key),
    bank_key INTEGER REFERENCES monetic.dim_bank(bank_key),
    customer_key BIGINT REFERENCES monetic.dim_customer(customer_key),
    card_key BIGINT REFERENCES monetic.dim_card(card_key),
    terminal_key INTEGER REFERENCES monetic.dim_terminal(terminal_key),
    merchant_key INTEGER REFERENCES monetic.dim_merchant(merchant_key),
    location_key INTEGER REFERENCES monetic.dim_location(location_key),
    transaction_type_key INTEGER REFERENCES monetic.dim_transaction_type(transaction_type_key),
    response_code_key INTEGER REFERENCES monetic.dim_response_code(response_code_key),
    transaction_timestamp TIMESTAMP NOT NULL,
    amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'XOF',
    processing_time_ms INTEGER,
    is_success BOOLEAN NOT NULL DEFAULT FALSE,
    is_suspicious BOOLEAN NOT NULL DEFAULT FALSE,
    channel VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monetic.fact_terminal_status (
    terminal_status_key BIGSERIAL PRIMARY KEY,
    terminal_key INTEGER NOT NULL REFERENCES monetic.dim_terminal(terminal_key),
    date_key INTEGER NOT NULL REFERENCES monetic.dim_date(date_key),
    status_timestamp TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    response_time_ms INTEGER,
    uptime_percentage NUMERIC(5,2),
    incident_flag BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monetic.fact_incidents (
    incident_key BIGSERIAL PRIMARY KEY,
    incident_id VARCHAR(50) NOT NULL UNIQUE,
    terminal_key INTEGER REFERENCES monetic.dim_terminal(terminal_key),
    bank_key INTEGER REFERENCES monetic.dim_bank(bank_key),
    date_key INTEGER REFERENCES monetic.dim_date(date_key),
    incident_timestamp TIMESTAMP NOT NULL,
    incident_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    status VARCHAR(20) DEFAULT 'OPEN',
    resolution_time_minutes INTEGER,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);