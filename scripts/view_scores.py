import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

# Load data
df = pd.read_sql("SELECT park_score FROM postcodes WHERE park_score IS NOT NULL", conn)
conn.close()

# Plot histogram
sns.histplot(df['park_score'], bins=50, kde=True)
plt.title("Distribution of Park Scores")
plt.xlabel("Park Score (0 to 1)")
plt.ylabel("Number of Postcodes")
plt.show()
