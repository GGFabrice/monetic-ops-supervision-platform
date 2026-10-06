-- ============================================================
-- KPI 1 : Nombre total d'incidents
-- ============================================================

SELECT
    COUNT(*) AS total_incidents
FROM monetic.fact_incidents;


-- ============================================================
-- KPI 2 : Nombre d'incidents critiques
-- ============================================================

SELECT
    COUNT(*) AS critical_incidents
FROM monetic.fact_incidents
WHERE severity = 'CRITICAL';


-- ============================================================
-- KPI 3 : Répartition des incidents par statut
-- ============================================================

SELECT
    status,
    COUNT(*) AS total_incidents,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM monetic.fact_incidents
GROUP BY status
ORDER BY total_incidents DESC;


-- ============================================================
-- KPI 4 : Répartition par gravité
-- ============================================================

SELECT
    severity,
    COUNT(*) AS total_incidents,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM monetic.fact_incidents
GROUP BY severity
ORDER BY
    CASE severity
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END;


-- ============================================================
-- KPI 5 : Répartition par type d'incident
-- ============================================================

SELECT
    incident_type,
    COUNT(*) AS total_incidents,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM monetic.fact_incidents
GROUP BY incident_type
ORDER BY total_incidents DESC;


-- ============================================================
-- KPI 6 : MTTR
-- Mean Time To Repair
-- Calculé uniquement sur les incidents résolus
-- ============================================================

SELECT
    COUNT(*) AS resolved_incidents,
    ROUND(
        AVG(resolution_time_minutes),
        2
    ) AS mttr_minutes,
    ROUND(
        AVG(resolution_time_minutes) / 60.0,
        2
    ) AS mttr_hours
FROM monetic.fact_incidents
WHERE status = 'RESOLVED';


-- ============================================================
-- KPI 7 : Durée minimale, moyenne et maximale
-- des incidents résolus
-- ============================================================

SELECT
    MIN(resolution_time_minutes)
        AS min_resolution_minutes,

    ROUND(
        AVG(resolution_time_minutes),
        2
    ) AS avg_resolution_minutes,

    MAX(resolution_time_minutes)
        AS max_resolution_minutes
FROM monetic.fact_incidents
WHERE status = 'RESOLVED';


-- ============================================================
-- KPI 8 : Incidents par mois
-- ============================================================

SELECT
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(*) AS total_incidents
FROM monetic.fact_incidents fi
JOIN monetic.dim_date dd
    ON dd.date_key = fi.date_key
GROUP BY
    dd.year,
    dd.month,
    dd.month_name
ORDER BY
    dd.year,
    dd.month;