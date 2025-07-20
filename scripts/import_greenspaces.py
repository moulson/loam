import geopandas as gpd
import psycopg2
from sqlalchemy import create_engine
import yaml

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    

# Read config
config = load_config()

gpkg_path = config['files']['greenspace']
db = config['database']
db_url =  f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['dbname']}" # e.g. postgresql+psycopg2://user:pass@localhost:5432/dbname

# Load greenspace_site layer
gdf = gpd.read_file(gpkg_path, layer="greenspace_site")

# Extract useful columns
gdf['name'] = gdf['distinctive_name_1']
gdf = gdf[['id', 'name', 'function', 'geometry']]
gdf.rename(columns={'id': 'source_id'}, inplace=True)

# Confirm correct CRS
gdf.set_crs(epsg=27700, inplace=True)

# Calculate area in square meters
gdf['park_sqm'] = gdf.geometry.area

# Upload to PostGIS
engine = create_engine(db_url)
gdf.to_postgis('parks', engine, if_exists='replace', index=False)

print("✅ Parks imported successfully.")