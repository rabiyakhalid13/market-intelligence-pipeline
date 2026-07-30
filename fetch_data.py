import requests
def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params={"ids":"bitcoin,ethereum,solana","vs_currencies":"usd"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__=="__main__":
    result=fetch_prices()
    print(result)
    