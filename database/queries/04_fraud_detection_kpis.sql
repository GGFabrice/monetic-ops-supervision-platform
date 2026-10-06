
-- ============================================================
-- 04 - FRAUD DETECTION KPIs
-- ============================================================

-- KPI 1 - Vue globale du scoring
SELECT
    COUNT(*) AS total_alerts,
    COUNT(DISTINCT transaction_key) AS unique_transactions,
    ROUND(AVG(risk_score), 2) AS average_risk_score,
    MIN(risk_score) AS min_risk_score,
    MAX(risk_score) AS max_risk_score,
    ROUND(SUM(transaction_amount), 2) AS total_amount
FROM monetic.fraud_alerts;

-- KPI 2 - RÃ©partition par niveau de risque
SELECT
    risk_level,
    COUNT(*) AS total_alerts,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage,
    ROUND(SUM(transaction_amount), 2) AS total_amount
FROM monetic.fraud_alerts
GROUP BY risk_level
ORDER BY CASE risk_level
    WHEN 'CRITICAL' THEN 1
    WHEN 'HIGH' THEN 2
    WHEN 'MEDIUM' THEN 3
    WHEN 'LOW' THEN 4
END;

-- KPI 3 - Exposition HIGH + CRITICAL
SELECT
    COUNT(*) AS high_critical_alerts,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM monetic.fraud_alerts),
        2
    ) AS high_critical_rate,
    ROUND(SUM(transaction_amount), 2) AS high_critical_amount,
    ROUND(
        SUM(transaction_amount) * 100.0 /
        (SELECT SUM(transaction_amount) FROM monetic.fraud_alerts),
        2
    ) AS high_critical_amount_rate
FROM monetic.fraud_alerts
WHERE risk_level IN ('HIGH', 'CRITICAL');

-- KPI 4 - Alertes HIGH + CRITICAL par banque
SELECT
    db.bank_name,
    COUNT(*) AS total_alerts,
    ROUND(SUM(fa.transaction_amount), 2) AS total_amount
FROM monetic.fraud_alerts fa
JOIN monetic.dim_bank db
    ON fa.bank_key = db.bank_key
WHERE fa.risk_level IN ('HIGH', 'CRITICAL')
GROUP BY db.bank_name
ORDER BY total_amount DESC;

-- KPI 5 - Alertes HIGH + CRITICAL par ville
SELECT
    dl.city,
    COUNT(*) AS total_alerts,
    ROUND(SUM(fa.transaction_amount), 2) AS total_amount
FROM monetic.fraud_alerts fa
JOIN monetic.dim_location dl
    ON fa.location_key = dl.location_key
WHERE fa.risk_level IN ('HIGH', 'CRITICAL')
GROUP BY dl.city
ORDER BY total_amount DESC;

-- KPI 6 - Alertes HIGH + CRITICAL par type de transaction
SELECT
    dtt.transaction_code,
    dtt.transaction_name,
    COUNT(*) AS total_alerts,
    ROUND(SUM(fa.transaction_amount), 2) AS total_amount
FROM monetic.fraud_alerts fa
JOIN monetic.dim_transaction_type dtt
    ON fa.transaction_type_key = dtt.transaction_type_key
WHERE fa.risk_level IN ('HIGH', 'CRITICAL')
GROUP BY dtt.transaction_code, dtt.transaction_name
ORDER BY total_amount DESC;

-- KPI 7 - Alertes par code rÃ©ponse
SELECT
    fa.response_code,
    COUNT(*) AS total_alerts,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage,
    ROUND(SUM(fa.transaction_amount), 2) AS total_amount
FROM monetic.fraud_alerts fa
GROUP BY fa.response_code
ORDER BY total_alerts DESC;

-- KPI 8 - Contribution des rÃ¨gles par niveau de risque
SELECT
    risk_level,
    SUM(CASE WHEN amount_score > 0 THEN 1 ELSE 0 END) AS amount_triggered,
    SUM(CASE WHEN unusual_hour_score > 0 THEN 1 ELSE 0 END) AS unusual_hour_triggered,
    SUM(CASE WHEN processing_time_score > 0 THEN 1 ELSE 0 END) AS processing_time_triggered,
    SUM(CASE WHEN response_code_score > 0 THEN 1 ELSE 0 END) AS response_code_triggered,
    SUM(CASE WHEN suspicious_flag_score > 0 THEN 1 ELSE 0 END) AS suspicious_flag_triggered
FROM monetic.fraud_alerts
GROUP BY risk_level
ORDER BY CASE risk_level
    WHEN 'CRITICAL' THEN 1
    WHEN 'HIGH' THEN 2
    WHEN 'MEDIUM' THEN 3
    WHEN 'LOW' THEN 4
END;

-- KPI 9 - Top 10 transactions les plus risquÃ©es
SELECT
    transaction_id,
    risk_score,
    risk_level,
    ROUND(transaction_amount, 2) AS transaction_amount,
    response_code,
    channel,
    alert_timestamp
FROM monetic.fraud_alerts
ORDER BY risk_score DESC, transaction_amount DESC
LIMIT 10;

-- KPI 10 - Distribution des scores
SELECT
    risk_score,
    COUNT(*) AS total_alerts,
    ROUND(SUM(transaction_amount), 2) AS total_amount
FROM monetic.fraud_alerts
GROUP BY risk_score
ORDER BY risk_score DESC;
