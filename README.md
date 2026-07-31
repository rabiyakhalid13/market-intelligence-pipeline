# Crypto Market Intelligence Dashboard

🔗 **Live Dashboard:** https://market-intelligence-pipeline-production.up.railway.app/

An end-to-end data pipeline that collects cryptocurrency market data, stores it in a MySQL database, performs exploratory analysis, and presents the results through an interactive Dash dashboard.

---

## Overview

Most beginner data science projects start with a static CSV file. This project takes a different approach by working with live market data and building the complete data pipeline around it.

The application fetches cryptocurrency prices from the CoinGecko API, stores them in a MySQL database, analyzes the collected data using Pandas, and visualizes the results in a web-based dashboard built with Dash. The deployed dashboard allows anyone to explore the data without installing the project locally.

---

## Features

* Fetches live cryptocurrency prices from the CoinGecko API
* Stores market data in a MySQL database
* Imports the previous 30 days of historical price data for analysis
* Interactive dashboard built with Dash and Plotly
* Live price cards for Bitcoin, Ethereum, and Solana
* Coin-specific trend visualization
* Daily average price analysis
* 30-day percentage change comparison
* Volatility comparison using standard deviation
* Searchable market data table
* Automation script for scheduled hourly data collection

## Screenshots

**Dashboard overview — live price cards and trend**
![Dashboard Overview](screenshots/dashboard-overview.png)

**Daily average comparison across coins**
![Daily Average](screenshots/daily-average.png)

**Volatility comparison**
![Volatility](screenshots/volatility.png)

---

## Project Workflow

```text
                  CoinGecko API
                        │
        ┌─-─────────────┴───────────────┐
        │                               │
 historical_data.py              fetch_data.py
        │                               │
        └───────────────┬───────────────┘
                        │
                  database.py
                        │
                     MySQL
                        │
         ┌──────────────┴──────────────┐
         │                             │
      eda.py                    dashboard.py
```

---

## Project Structure

```text
market-intelligence-pipeline/
│
├── fetch_data.py         # Fetches live cryptocurrency prices
├── database.py           # Database connection and insert logic
├── historical_data.py    # Imports 30 days of historical market data
├── scheduler.py          # Automates hourly data collection
├── eda.py                # Data analysis and visualizations
├── dashboard.py          # Dash application
├── requirements.txt
└── .gitignore
```

---

## How the Pipeline Works

### 1. Data Collection

`fetch_data.py` retrieves the latest prices of Bitcoin, Ethereum, and Solana from the CoinGecko API. Basic error handling is included to manage temporary connection or API issues.

### 2. Database Storage

`database.py` manages the MySQL connection and inserts each price record into the database with an associated timestamp.

### 3. Historical Data Import

Instead of waiting several weeks to accumulate enough observations, `historical_data.py` imports the previous 30 days of hourly cryptocurrency prices directly from the CoinGecko historical endpoint. This provides a meaningful dataset for analysis while using the same database structure as the live pipeline.

### 4. Scheduled Data Collection

`scheduler.py` demonstrates how the pipeline can automatically collect fresh market data at regular intervals using Python's `schedule` library.

For this portfolio version, the scheduler is intentionally not running continuously in production. Historical data was used instead of maintaining a long-running background process, making the project practical to deploy on a free hosting platform while preserving the complete automation logic.

### 5. Data Analysis

`eda.py` performs exploratory data analysis using Pandas, including:

* Daily average prices
* 30-day percentage price change
* Volatility comparison using standard deviation

The analysis is visualized using Plotly charts.

### 6. Interactive Dashboard

`dashboard.py` connects directly to the MySQL database and provides an interactive interface for exploring cryptocurrency data. Users can:

* View current prices
* Select individual cryptocurrencies
* Explore historical trends
* Compare market performance
* Search through stored market records

---

## Technology Stack

| Category             | Technologies  |
| -------------------- | ------------- |
| Programming Language | Python        |
| API                  | CoinGecko API |
| Database             | MySQL         |
| Data Analysis        | Pandas        |
| Visualization        | Plotly        |
| Dashboard            | Dash          |
| Deployment           | Railway       |
| Version Control      | Git & GitHub  |

---

## Skills Demonstrated

* REST API Integration
* ETL Pipeline Development
* Relational Database Management
* Exploratory Data Analysis (EDA)
* Interactive Dashboard Development
* Data Visualization
* Deployment with Railway
* Git Version Control

---

## Running the Project Locally

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your database credentials:

```env
DB_HOST=your_host
DB_PORT=your_port
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```

Run the dashboard:

```bash
python dashboard.py
```

---

## Future Improvements

* Enable continuous real-time data collection through scheduled background jobs
* Track additional cryptocurrencies
* Add automated unit tests

---

