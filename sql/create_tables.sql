CREATE TABLE postcodes(
    id SERIAL PRIMARY KEY,
    postcode VARCHAR(8) UNIQUE NOT NULL,
    town VARCHAR(128),
    oa CHAR(9),
    lsoa CHAR(9),
    msoa CHAR(9),
    imd INTEGER,
    oslaua CHAR(9),
    osward CHAR(9),
    lat DOUBLE PRECISION,
    long DOUBLE PRECISION,
    location GEOGRAPHY(Point, 4326),
    park_sqm DOUBLE PRECISION,
    park_score DOUBLE PRECISION
);