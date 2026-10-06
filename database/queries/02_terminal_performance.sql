-- ============================================================
-- TERMINAL PERFORMANCE & SUPERVISION
-- ============================================================


-- ============================================================
-- KPI 1 : Nombre d'incidents par terminal
-- ============================================================

SELECT
    dt.terminal_id,
    dt.terminal_type,
    dt.city,
    COUNT(fi.incident_key) AS total_incidents,
    COUNT(*) FILTER (
        WHERE fi.severity = 'CRITICAL'
    ) AS critical_incidents,
    COUNT(*) FILTER (
        WHERE fi.severity = 'HIGH'
    ) AS high_incidents,
    COUNT(*) FILTER (
        WHERE fi.severity = 'MEDIUM'
    ) AS medium_incidents
FROM monetic.dim_terminal dt
LEFT JOIN monetic.fact_incidents fi
    ON fi.terminal_key = dt.terminal_key
GROUP BY
    dt.terminal_id,
    dt.terminal_type,
    dt.city
ORDER BY
    total_incidents DESC;


-- ============================================================
-- KPI 2 : Top 10 terminaux les plus problématiques
-- ============================================================

SELECT
    dt.terminal_id,
    dt.terminal_type,
    dt.city,
    COUNT(fi.incident_key) AS total_incidents,
    COUNT(*) FILTER (
        WHERE fi.severity = 'CRITICAL'
    ) AS critical_incidents
FROM monetic.dim_terminal dt
LEFT JOIN monetic.fact_incidents fi
    ON fi.terminal_key = dt.terminal_key
GROUP BY
    dt.terminal_id,
    dt.terminal_type,
    dt.city
ORDER BY
    total_incidents DESC,
    critical_incidents DESC
LIMIT 10;


-- ============================================================
-- KPI 3 : Disponibilité moyenne par terminal
-- ============================================================

SELECT
    dt.terminal_id,
    dt.terminal_type,
    dt.city,
    ROUND(
        AVG(fts.uptime_percentage),
        2
    ) AS avg_uptime_percentage
FROM monetic.dim_terminal dt
JOIN monetic.fact_terminal_status fts
    ON fts.terminal_key = dt.terminal_key
GROUP BY
    dt.terminal_id,
    dt.terminal_type,
    dt.city
ORDER BY
    avg_uptime_percentage ASC;


-- ============================================================
-- KPI 4 : Temps de réponse moyen par terminal
-- ============================================================

SELECT
    dt.terminal_id,
    dt.terminal_type,
    dt.city,
    ROUND(
        AVG(fts.response_time_ms),
        2
    ) AS avg_response_time_ms,
    MIN(fts.response_time_ms)
        AS min_response_time_ms,
    MAX(fts.response_time_ms)
        AS max_response_time_ms
FROM monetic.dim_terminal dt
JOIN monetic.fact_terminal_status fts
    ON fts.terminal_key = dt.terminal_key
WHERE fts.response_time_ms IS NOT NULL
GROUP BY
    dt.terminal_id,
    dt.terminal_type,
    dt.city
ORDER BY
    avg_response_time_ms DESC;


-- ============================================================
-- KPI 5 : Nombre d'observations par statut
-- ============================================================

SELECT
    dt.terminal_type,
    fts.status,
    COUNT(*) AS total_observations,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (
            PARTITION BY dt.terminal_type
        ),
        2
    ) AS percentage
FROM monetic.fact_terminal_status fts
JOIN monetic.dim_terminal dt
    ON dt.terminal_key = fts.terminal_key
GROUP BY
    dt.terminal_type,
    fts.status
ORDER BY
    dt.terminal_type,
    total_observations DESC;


-- ============================================================
-- KPI 6 : Performance ATM vs POS
-- ============================================================

SELECT
    dt.terminal_type,
    COUNT(DISTINCT dt.terminal_key)
        AS total_terminals,

    COUNT(DISTINCT fi.incident_key)
        AS total_incidents,

    ROUND(
        AVG(fts.uptime_percentage),
        2
    ) AS avg_uptime_percentage,

    ROUND(
        AVG(fts.response_time_ms),
        2
    ) AS avg_response_time_ms

FROM monetic.dim_terminal dt

LEFT JOIN monetic.fact_terminal_status fts
    ON fts.terminal_key = dt.terminal_key

LEFT JOIN monetic.fact_incidents fi
    ON fi.terminal_key = dt.terminal_key

GROUP BY
    dt.terminal_type

ORDER BY
    dt.terminal_type;


-- ============================================================
-- KPI 7 : Terminaux avec incidents critiques
-- ============================================================

SELECT
    dt.terminal_id,
    dt.terminal_type,
    dt.city,
    COUNT(fi.incident_key) AS critical_incidents
FROM monetic.dim_terminal dt
JOIN monetic.fact_incidents fi
    ON fi.terminal_key = dt.terminal_key
WHERE fi.severity = 'CRITICAL'
GROUP BY
    dt.terminal_id,
    dt.terminal_type,
    dt.city
ORDER BY
    critical_incidents DESC;


-- ============================================================
-- KPI 8 : Incidents par ville
-- ============================================================

SELECT
    dt.city,
    COUNT(fi.incident_key) AS total_incidents,
    COUNT(*) FILTER (
        WHERE fi.severity = 'CRITICAL'
    ) AS critical_incidents
FROM monetic.dim_terminal dt
JOIN monetic.fact_incidents fi
    ON fi.terminal_key = dt.terminal_key
GROUP BY
    dt.city
ORDER BY
    total_incidents DESC;