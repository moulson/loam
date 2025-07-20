from tqdm import tqdm
import psycopg2
import yaml;

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()
db = config['database']
conn = psycopg2.connect(
    dbname=db['dbname'],
    user=db['user'],
    password=db['password'],
    host=db['host'],
    port=db['port']
)
cur = conn.cursor()

# Get max ID
cur.execute("SELECT MAX(id) FROM postcodes;")
max_id = cur.fetchone()[0]
batch_size = 10000

for start in tqdm(range(1, max_id + 1, batch_size)):
    end = start + batch_size - 1

    cur.execute("""
        UPDATE postcodes p
        SET park_sqm = sub.total_area
        FROM (
            SELECT p.id AS postcode_id,
                   SUM(ST_Area(parks.geog)) AS total_area
            FROM postcodes p
            JOIN parks
              ON ST_DWithin(p.location, parks.geog, 500)
            WHERE p.id BETWEEN %s AND %s
            GROUP BY p.id
        ) sub
        WHERE p.id = sub.postcode_id;
    """, (start, end))
    conn.commit()

cur.close()
conn.close()
