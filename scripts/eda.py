import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('LOCAL_DB_PASSWORD'),
    database="crypto_data"
)
cursor=conn.cursor()
cursor.execute("SELECT coin_name, price, timestamp FROM Prices")
data=cursor.fetchall()
df=pd.DataFrame(data,columns=['coin_name','price','timestamp'])

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)
print("\nFirst 5 rows:\n", df.head())

print("\n" + "=" * 50)
print("Columns are \n", df.columns)

print("\n" + "=" * 50)
print("\nDatatypes of columns\n", df.dtypes)

df['price'] = df['price'].astype(float)
print("\nPrice column converted to float")
print(df.dtypes)

print("\n" + "=" * 50)
print("DATASET INFO")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("STATISTICAL SUMMARY")
print("=" * 50)
print(df.describe())

print("\n" + "=" * 50)
print("MISSING VALUES CHECK")
print("=" * 50)
print(df.isnull().sum())

# Grouping data
print("\n" + "=" * 50)
print("Grouping data with coin names and display average,min and max values")
print(df.groupby('coin_name')['price'].agg(['mean','min','max']))
print("\n" + "=" * 50)

# Daily avg per coin
print("\n" + "=" * 50)
print('dislaying Daily avg per coin')
df['date']=df['timestamp'].dt.date
df1=df.groupby(['coin_name','date'])['price'].mean()
print(df1)
print("\n" + "=" * 50)

print("\n" + "=" * 50)
print("AVERAGE OF COIN FOR 30 DAYS")
df1 = df.groupby(['coin_name', 'date'])['price'].mean().reset_index()
df1 = df1.sort_values(['coin_name', 'date'])

first_price = df1.groupby('coin_name').first()['price']
last_price = df1.groupby('coin_name').last()['price']

percentage_change = ((last_price - first_price) / first_price) * 100
percentage_change=percentage_change.round(2)
print(percentage_change)
print("\n" + "=" * 50)

print("\n" + "=" * 50)
print("\nTop performer:", percentage_change.idxmax(), f"({percentage_change.max()}%)")
print("Worst performer:", percentage_change.idxmin(), f"({percentage_change.min()}%)")
print("\n" + "=" * 50)

# GRAPHS
# PRICE TREND OF ALL COINS
fig = px.line(df, x='timestamp', y='price', color='coin_name', 
              title='Crypto Price Trend (Hourly) — Last 30 Days',
              labels={'timestamp': 'Date & Time', 'price': 'Price (USD)', 'coin_name': 'Cryptocurrency'},
              log_y=True)
fig.show()

# Daily average trend 
fig = px.line(df1, x='date', y='price', color='coin_name', 
              title='Daily Average Price Trend — Last 30 Days',
              labels={'date': 'Date', 'price': 'Average Price (USD)', 'coin_name': 'Cryptocurrency'},
              log_y=True)
fig.show()

# Percentage change comparison
pct_df = percentage_change.reset_index()
pct_df.columns = ['coin_name', 'percentage_change']
fig = px.bar(pct_df, x='coin_name', y='percentage_change', 
             title='30-Day Percentage Change by Coin',
             labels={'coin_name': 'Cryptocurrency', 'percentage_change': 'Change (%)'},
             text='percentage_change', color='coin_name')
fig.show()

# Single coin trend
bitcoin_df = df[df['coin_name'] == 'bitcoin']
fig = px.line(bitcoin_df, x='timestamp', y='price', 
              title='Bitcoin Price Trend — Last 30 Days',
              labels={'timestamp': 'Date & Time', 'price': 'Price (USD)'})
fig.show()

# Volatility calculation
deviation = df1.groupby('coin_name')['price'].std()
d_df = deviation.reset_index()
d_df.columns = ['coin_name', 'volatility']
fig = px.bar(d_df, x='coin_name', y='volatility', 
             title='Price Volatility Comparison Across Coins (Std. Deviation)',
             labels={'coin_name': 'Cryptocurrency', 'volatility': 'Volatility (USD)'},
             color='coin_name')
fig.show()