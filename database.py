import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('DB_PASSWORD'),
    database="crypto_data"
)
if conn.is_connected():
    print("Connected successfully!")

def insert_data(data):
    cursor=conn.cursor()
    for coin_name,price_info in data.items():
        query="INSERT INTO Prices(coin_name,price,timestamp) values(%s,%s,%s)"
        cursor.execute(query, (coin_name,price_info['usd'],datetime.now()))
    conn.commit()
    cursor.close()

from fetch_data import fetch_prices
if __name__=="__main__":
    data=fetch_prices()
    insert_data(data)
    print("Data inserted successfully!")   
    conn.close()
    print("Connection closed!")

