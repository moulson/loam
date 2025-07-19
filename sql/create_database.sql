-- Note that this can't be run as a script but should instead be run direct in the CLI

CREATE DATABASE loam;
\c loam;
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;