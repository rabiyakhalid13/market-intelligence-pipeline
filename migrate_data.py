import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# ---- Local database connection
local_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('DB_PASSWORD'),
    database="crypto_data"
)
local_cursor = local_conn.cursor()

# ---- Railway cloud database connection----
cloud_conn = mysql.connector.connect(
    host="sakura.proxy.rlwy.net",
    port=30155,
    user="root",
    password="HKDfhwTXTgoOCyThVIzaQykojnmVCmtS",
    database="railway",
    connection_timeout=10
)
cloud_cursor = cloud_conn.cursor()
print("Cloud connected!")


local_cursor.execute("SELECT coin_name, price, timestamp FROM Prices")
all_data = local_cursor.fetchall()
print(f"fetch {len(all_data)}  rowns from local")


insert_query = "INSERT INTO Prices (coin_name, price, timestamp) VALUES (%s, %s, %s)"
cloud_cursor.executemany(insert_query, all_data)
print("Insert complete, commit in process...")

cloud_conn.commit()
print(f"{len(all_data)} Migrate rows into Railway cloud database ")

local_cursor.close()
local_conn.close()
cloud_cursor.close()
cloud_conn.close()