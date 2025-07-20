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

CREATE TABLE parks (
    id SERIAL PRIMARY KEY,
    source_id INTEGER,
    name TEXT,
    function TEXT,
    park_sqm DOUBLE PRECISION,
    geometry GEOMETRY(MultiPolygon, 27700)
);

--After running import scripts
ALTER TABLE parks ADD COLUMN geog GEOGRAPHY(MultiPolygon, 4326);
UPDATE parks
SET geog = ST_Transform(geometry, 4326);

CREATE INDEX IF NOT EXISTS idx_postcodes_location ON postcodes USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_parks_geog ON parks USING GIST(geog);