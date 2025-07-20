UPDATE postcodes p
SET park_sqm = sub.total_area
FROM(
    SELECT
        p.id AS postcode_id,
        SUM(ST_Area(parks.geog)) AS total_area
    FROM postcodes p
    JOIN parks
        ON ST_DWithin(p.location, parks.geography, 500) -- 500 metres
    GROUP BY p.id
) sub
WHERE p.id = sub.postcode_id;

--normalize park_score
WITH stats AS(
    SELECT
        percentile_cont(ARRAY[0.25, 0.5, 0.75, 0.9, 0.99])
        WITHIN GROUP (ORDER BY park_sqm) AS percentiles
    FROM postcodes
    WHERE park_sqm IS NOT NULL
), p AS (
    SELECT *,
        NTILE(100) OVER (ORDER BY park_sqm) AS percentile_rank
    FROM postcodes
)
UPDATE postcodes
SET park_score = p.percentile_rank / 100.0
FROM p
WHERE postcodes.id = p.id