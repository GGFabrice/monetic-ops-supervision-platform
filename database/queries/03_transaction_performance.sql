-- ============================================================
-- TRANSACTION PERFORMANCE & ANALYTICS
-- ============================================================

-- KPI 1 : Vue globale des transactions
SELECT
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount,
    ROUND(MIN(amount), 2) AS min_amount,
    ROUND(MAX(amount), 2) AS max_amount
FROM monetic.fact_transactions;


-- KPI 2 : Transactions réussies vs rejetées
SELECT
    CASE
        WHEN is_success THEN 'SUCCESS'
        ELSE 'REJECTED'
    END AS transaction_status,
    COUNT(*) AS total_transactions,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage,
    ROUND(SUM(amount), 2) AS total_amount
FROM monetic.fact_transactions
GROUP BY is_success
ORDER BY total_transactions DESC;


-- KPI 3 : Transactions suspectes
SELECT
    COUNT(*) FILTER (
        WHERE is_suspicious
    ) AS suspicious_transactions,
    ROUND(
        SUM(amount) FILTER (
            WHERE is_suspicious
        ),
        2
    ) AS suspicious_amount,
    ROUND(
        COUNT(*) FILTER (
            WHERE is_suspicious
        ) * 100.0 / COUNT(*),
        2
    ) AS suspicious_rate_percentage
FROM monetic.fact_transactions;


-- KPI 4 : Performance par type de transaction
SELECT
    dtt.transaction_code,
    dtt.transaction_name,
    dtt.channel,
    COUNT(ft.transaction_key) AS total_transactions,
    ROUND(SUM(ft.amount), 2) AS total_amount,
    ROUND(AVG(ft.amount), 2) AS average_amount,
    ROUND(
        COUNT(*) FILTER (
            WHERE ft.is_success
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percentage
FROM monetic.fact_transactions ft
JOIN monetic.dim_transaction_type dtt
    ON dtt.transaction_type_key = ft.transaction_type_key
GROUP BY
    dtt.transaction_code,
    dtt.transaction_name,
    dtt.channel
ORDER BY total_transactions DESC;


-- KPI 5 : Performance par banque
SELECT
    db.bank_code,
    db.bank_name,
    COUNT(ft.transaction_key) AS total_transactions,
    ROUND(SUM(ft.amount), 2) AS total_amount,
    ROUND(
        COUNT(*) FILTER (
            WHERE ft.is_success
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percentage,
    ROUND(
        COUNT(*) FILTER (
            WHERE ft.is_suspicious
        ) * 100.0 / COUNT(*),
        2
    ) AS suspicious_rate_percentage
FROM monetic.fact_transactions ft
JOIN monetic.dim_bank db
    ON db.bank_key = ft.bank_key
GROUP BY
    db.bank_code,
    db.bank_name
ORDER BY total_transactions DESC;


-- KPI 6 : Analyse des codes de réponse
SELECT
    drc.response_code,
    drc.response_label,
    drc.response_category,
    drc.is_success,
    COUNT(ft.transaction_key) AS total_transactions,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage,
    ROUND(SUM(ft.amount), 2) AS total_amount
FROM monetic.fact_transactions ft
JOIN monetic.dim_response_code drc
    ON drc.response_code_key = ft.response_code_key
GROUP BY
    drc.response_code,
    drc.response_label,
    drc.response_category,
    drc.is_success
ORDER BY total_transactions DESC;


-- KPI 7 : Performance par ville
SELECT
    dl.city,
    dl.region,
    COUNT(ft.transaction_key) AS total_transactions,
    ROUND(SUM(ft.amount), 2) AS total_amount,
    ROUND(
        COUNT(*) FILTER (
            WHERE ft.is_success
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percentage,
    COUNT(*) FILTER (
        WHERE ft.is_suspicious
    ) AS suspicious_transactions
FROM monetic.fact_transactions ft
JOIN monetic.dim_location dl
    ON dl.location_key = ft.location_key
GROUP BY
    dl.city,
    dl.region
ORDER BY total_transactions DESC;


-- KPI 8 : Évolution mensuelle
SELECT
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(ft.transaction_key) AS total_transactions,
    ROUND(SUM(ft.amount), 2) AS total_amount,
    ROUND(
        COUNT(*) FILTER (
            WHERE ft.is_success
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percentage,
    COUNT(*) FILTER (
        WHERE ft.is_suspicious
    ) AS suspicious_transactions
FROM monetic.fact_transactions ft
JOIN monetic.dim_date dd
    ON dd.date_key = ft.date_key
GROUP BY
    dd.year,
    dd.month,
    dd.month_name
ORDER BY
    dd.year,
    dd.month;


-- KPI 9 : Analyse horaire
SELECT
    EXTRACT(HOUR FROM transaction_timestamp)::INTEGER AS transaction_hour,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(
        COUNT(*) FILTER (
            WHERE is_success
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percentage,
    COUNT(*) FILTER (
        WHERE is_suspicious
    ) AS suspicious_transactions
FROM monetic.fact_transactions
GROUP BY
    EXTRACT(HOUR FROM transaction_timestamp)
ORDER BY transaction_hour;


-- KPI 10 : Transactions suspectes à montant élevé
SELECT
    ft.transaction_id,
    ft.transaction_timestamp,
    ft.amount,
    ft.currency,
    ft.channel,
    db.bank_code,
    dtt.transaction_code,
    drc.response_code,
    dl.city,
    ft.processing_time_ms
FROM monetic.fact_transactions ft
LEFT JOIN monetic.dim_bank db
    ON db.bank_key = ft.bank_key
LEFT JOIN monetic.dim_transaction_type dtt
    ON dtt.transaction_type_key = ft.transaction_type_key
LEFT JOIN monetic.dim_response_code drc
    ON drc.response_code_key = ft.response_code_key
LEFT JOIN monetic.dim_location dl
    ON dl.location_key = ft.location_key
WHERE ft.is_suspicious = TRUE
ORDER BY ft.amount DESC
LIMIT 20;