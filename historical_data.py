import requests
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('DB_PASSWORD'),
    database="crypto_data"
)

def fetch_historical(coin_name,days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart"
    params={"vs_currency":"usd","days":days}
    response=requests.get(url,params=params)
    data=response.json()
    return data['prices']

def insert_historical(coin_name,prices):
    cursor=conn.cursor()
    for timestamp,price in prices:
        readable_time = datetime.fromtimestamp(timestamp / 1000)
        query="INSERT INTO Prices(coin_name,price,timestamp) values(%s,%s,%s)"
        cursor.execute(query, (coin_name,price,readable_time))
    conn.commit()
    cursor.close()

if __name__=="__main__":
    coins={"bitcoin","ethereum","solana"}
    for coin in coins:
        prices=fetch_historical(coin,days=30)
        insert_historical(coin,prices)
        print(f"{coin}:{len(prices)} records inserted")
    conn.close()
    print("Connection closed!")
    print("Historical data fetched and inserted!")
