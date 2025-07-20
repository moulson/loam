WITH stats AS (
    SELECT
        MIN(park_sqm) AS min_val
        ,MAX(park_sqm) AS max_val
    FROM postcodes
    WHERE park_sqm IS NOT NULL
)
UPDATE postcodes
SET park_score = CASE
    WHEN stats.max_val = stats.min_val THEN 0.0
    ELSE (park_sqm - stats.min_val) / (stats.max_val - stats.min_val)
END
FROM stats
WHERE park_sqm IS NOT NULL