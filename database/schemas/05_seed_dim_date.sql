INSERT INTO monetic.dim_date
(
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    day_of_week,
    day_name,
    week_of_year,
    is_weekend
)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER AS date_key,
    d::DATE AS full_date,
    EXTRACT(DAY FROM d)::INTEGER AS day,
    EXTRACT(MONTH FROM d)::INTEGER AS month,
    TO_CHAR(d, 'TMMonth') AS month_name,
    EXTRACT(QUARTER FROM d)::INTEGER AS quarter,
    EXTRACT(YEAR FROM d)::INTEGER AS year,
    EXTRACT(ISODOW FROM d)::INTEGER AS day_of_week,
    TO_CHAR(d, 'TMDay') AS day_name,
    EXTRACT(WEEK FROM d)::INTEGER AS week_of_year,
    CASE
        WHEN EXTRACT(ISODOW FROM d) IN (6, 7)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM generate_series(
    DATE '2026-01-01',
    DATE '2026-12-31',
    INTERVAL '1 day'
) AS d
ON CONFLICT (date_key) DO NOTHING;