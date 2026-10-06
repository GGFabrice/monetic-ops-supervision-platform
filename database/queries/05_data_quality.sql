-- ============================================================
-- 05 - DATA QUALITY CHECKS
-- ============================================================

-- KPI 1 : volume des transactions
SELECT
    'fact_transactions' AS table_name,
    COUNT(*) AS total_rows
FROM monetic.fact_transactions;

-- KPI 2 : transactions avec clés obligatoires manquantes
SELECT
    COUNT(*) AS invalid_transactions
FROM monetic.fact_transactions
WHERE transaction_id IS NULL
   OR transaction_timestamp IS NULL
   OR date_key IS NULL;

-- KPI 3 : transactions sans localisation
SELECT
    COUNT(*) AS transactions_without_location
FROM monetic.fact_transactions
WHERE location_key IS NULL;

-- KPI 4 : transactions avec montant négatif
SELECT
    COUNT(*) AS negative_amounts
FROM monetic.fact_transactions
WHERE amount < 0;

-- KPI 5 : scores de risque invalides
SELECT
    COUNT(*) AS invalid_risk_scores
FROM monetic.fraud_alerts
WHERE risk_score < 0
   OR risk_score > 100;

-- KPI 6 : niveaux de risque invalides
SELECT
    COUNT(*) AS invalid_risk_levels
FROM monetic.fraud_alerts
WHERE risk_level NOT IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');

-- KPI 7 : alertes sans transaction correspondante
SELECT
    COUNT(*) AS orphan_alerts
FROM monetic.fraud_alerts fa
LEFT JOIN monetic.fact_transactions ft
    ON fa.transaction_key = ft.transaction_key
WHERE ft.transaction_key IS NULL;

-- KPI 8 : doublons transaction_id
SELECT
    COUNT(*) AS duplicate_transaction_ids
FROM (
    SELECT transaction_id
    FROM monetic.fact_transactions
    GROUP BY transaction_id
    HAVING COUNT(*) > 1
) duplicates;

-- KPI 9 : cohérence succès / code réponse
SELECT
    COUNT(*) AS inconsistent_success_flags
FROM monetic.fact_transactions ft
JOIN monetic.dim_response_code rc
    ON ft.response_code_key = rc.response_code_key
WHERE ft.is_success <> rc.is_success;

-- KPI 10 : cohérence des alertes avec les transactions
SELECT
    COUNT(*) AS inconsistent_alert_amounts
FROM monetic.fraud_alerts fa
JOIN monetic.fact_transactions ft
    ON fa.transaction_key = ft.transaction_key
WHERE fa.transaction_amount <> ft.amount;