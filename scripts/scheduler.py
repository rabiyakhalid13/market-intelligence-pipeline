
from fetch_data import fetch_prices
from database import insert_data
import schedule
import time

def job():
    data=fetch_prices()
    insert_data(data)
    print("Data fetched and inserted!")

schedule.every(1).hours.do(job)
while True:
    schedule.run_pending()
    time.sleep(60)