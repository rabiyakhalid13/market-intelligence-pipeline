from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
from fetch_data import fetch_prices

# 1. DATA LOADING 
load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
    )
cursor = conn.cursor()
cursor.execute("SELECT coin_name, price, timestamp FROM Prices")
data = cursor.fetchall()

df = pd.DataFrame(data, columns=['coin_name', 'price', 'timestamp'])
df['price'] = df['price'].astype(float)
df['timestamp'] = pd.to_datetime(df['timestamp']) 
df = df.sort_values(['coin_name', 'timestamp'])
df['date'] = df['timestamp'].dt.date

# 2. CALCULATIONS 
df1 = df.groupby(['coin_name', 'date'])['price'].mean().reset_index()
df1 = df1.sort_values(['coin_name', 'date'])

first_price = df1.groupby('coin_name').first()['price']
last_price = df1.groupby('coin_name').last()['price']
percentage_change = ((last_price - first_price) / first_price * 100).round(2)
pct_df = percentage_change.reset_index()
pct_df.columns = ['coin_name', 'percentage_change']

deviation = df1.groupby('coin_name')['price'].std()
d_df = deviation.reset_index()
d_df.columns = ['coin_name', 'volatility']

# 3. LIVE PRICES 

live_prices = fetch_prices()

# 4. STATIC GRAPHS 
daily_fig = px.line(df1, x='date', y='price', color='coin_name',
                     title='Daily Average Price Trend — Last 30 Days', log_y=True)

pct_fig = px.bar(pct_df, x='coin_name', y='percentage_change',
                  title='30-Day Percentage Change by Coin',
                  text='percentage_change', color='coin_name')

vol_fig = px.bar(d_df, x='coin_name', y='volatility',
                  title='Price Volatility Comparison Across Coins',
                  color='coin_name')

# 5. TOP/WORST PERFORMER TEXT
top_coin = percentage_change.idxmax()
worst_coin = percentage_change.idxmin()
summary_text = f"Top performer: {top_coin.capitalize()} ({percentage_change.max()}%) | Worst performer: {worst_coin.capitalize()} ({percentage_change.min()}%)"

# 6. DASH APP + LAYOUT
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Crypto Market Intelligence Dashboard", style={'textAlign': 'center'}),

    html.P(f"Data range: {df['date'].min()} to {df['date'].max()}", 
       style={'textAlign': 'center', 'color': 'gray'}),

    html.Div(id='price-cards'),

    html.P(summary_text, style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '20px'}),

    html.H3("Select a Coin", style={'marginTop': '30px'}),
    dcc.Dropdown(
        id='coin-dropdown',
        options=[{'label': c.capitalize(), 'value': c} for c in df['coin_name'].unique()],
        value='bitcoin'
    ),

    dcc.Graph(id='selected-coin-graph'),

    html.H3("Daily Average Trend (All Coins)"),
    dcc.Graph(figure=daily_fig),

    html.H3("Percentage Change Comparison"),
    dcc.Graph(figure=pct_fig),

    html.H3("Volatility Comparison"),
    dcc.Graph(figure=vol_fig),

    html.H3("Data Table"),
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in ['coin_name', 'price', 'timestamp']],
        page_size=10,
        filter_action='native',
        sort_action='native'
    )
], style={'maxWidth': '1000px', 'margin': 'auto', 'fontFamily': 'Arial'})

# 7. CALLBACKS

@app.callback(
    Output('price-cards', 'children'),
    Input('coin-dropdown', 'value')
)
def update_cards(selected_coin):
    coins = ['bitcoin', 'ethereum', 'solana']
    cards = []
    for coin in coins:
        is_selected = (coin == selected_coin)
        cards.append(
            html.Div([
                html.H4(coin.capitalize()),
                html.H2(f"${live_prices[coin]['usd']:,}")
            ], style={
                'border': '3px solid #007bff' if is_selected else '1px solid #ccc',
                'background': '#e6f2ff' if is_selected else 'white',
                'padding': '20px', 'width': '30%', 'borderRadius': '10px'
            })
        )
    return html.Div(cards, style={'display': 'flex', 'justify-content': 'space-around'})


@app.callback(
    Output('selected-coin-graph', 'figure'),
    Input('coin-dropdown', 'value')
)
def update_graph(selected_coin):
    filtered_df = df[df['coin_name'] == selected_coin]
    fig = px.line(filtered_df, x='timestamp', y='price',
                   title=f'{selected_coin.capitalize()} Price Trend — Hourly Data, Last 30 Days')
    return fig


@app.callback(
    Output('data-table', 'data'),
    Input('coin-dropdown', 'value')
)
def update_table(selected_coin):
    filtered_df = df[df['coin_name'] == selected_coin][['coin_name', 'price', 'timestamp']]
    return filtered_df.to_dict('records')


# ============================================================
# 8. RUN APP
# ============================================================
server = app.server
if __name__ == "__main__":
    app.run(debug=True)
    