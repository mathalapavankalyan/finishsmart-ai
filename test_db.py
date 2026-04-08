import psycopg2

# Replace these with your AlloyDB info
DB_HOST = "10.10.0.2"          # From gcloud alloydb instances describe
DB_PORT = 5432                  # Default Postgres port
DB_NAME = "postgres"            # Default database
DB_USER = "postgres"
DB_PASSWORD = "root@123"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()
    print("Connection successful! Current time in DB:", result)
    cur.close()
    conn.close()
except Exception as e:
    print("Error connecting to DB:", e)