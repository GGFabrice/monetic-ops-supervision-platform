INSERT INTO monetic.dim_location
(
    city,
    district,
    region,
    country
)
SELECT
    v.city,
    v.district,
    v.region,
    v.country
FROM
(
    VALUES
        ('Bouaké', 'Gbêkê', 'Gbêkê', 'Côte d''Ivoire'),
        ('San-Pédro', 'San-Pédro', 'San-Pédro', 'Côte d''Ivoire')
) AS v(city, district, region, country)
WHERE NOT EXISTS
(
    SELECT 1
    FROM monetic.dim_location l
    WHERE l.city = v.city
);