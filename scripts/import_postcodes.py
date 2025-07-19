import csv
import yaml
import psycopg2
from psycopg2.extras import execute_values

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
def insert_batch(cur, batch):
    values = [
        r + (f'SRID=4326;POINT({r[9]} {r[8]})',)  # long lat → WKT POINT
        for r in batch
    ]

    insert_sql = """
        INSERT INTO postcodes (
            postcode, town, oa, lsoa, msoa, imd,
            oslaua, osward, lat, long, location
        )
        VALUES %s
        ON CONFLICT (postcode) DO NOTHING;
    """

    execute_values(cur, insert_sql, values)
    
def main():
    config = load_config()
    db = config['database']
    csv_path = config['files']['postcode_csv']

    conn = psycopg2.connect(
        dbname=db['dbname'],
        user=db['user'],
        password=db['password'],
        host=db['host'],
        port=db['port']
    )
    cur = conn.cursor()

    BATCH_SIZE = 10000
    batch = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, 1):
            try:
                postcode = row['pcds']
                town = None
                oa = row['oa21']
                lsoa = row['lsoa21']
                msoa = row['msoa21']
                imd = int(row['imd']) if row['imd'].isdigit() else None
                oslaua = row['oslaua']
                osward = row['osward']
                lat = float(row['lat']) if row['lat'] else None
                lon = float(row['long']) if row['long'] else None

                if lat is None or lon is None:
                    continue

                batch.append((
                    postcode, town, oa, lsoa, msoa, imd,
                    oslaua, osward, lat, lon
                ))

                if i % BATCH_SIZE == 0:
                    insert_batch(cur, batch)
                    conn.commit()
                    print(f"Inserted {i} rows...")
                    batch.clear()

            except Exception as e:
                print(f"Error at row {i}: {e}")
                continue

    # Final batch
    if batch:
        insert_batch(cur, batch)
        conn.commit()
        print(f"Final insert: {len(batch)} rows")


if __name__ == "__main__":
    main()
