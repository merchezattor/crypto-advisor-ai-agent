import os
import requests
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

def fetch_coinmarketcap_global_data() -> dict:
    """
    Fetches global market data from CoinMarketCap.
    Returns a dictionary with total market cap, 24h volume, and BTC dominance.
    """
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raise an error for bad responses
    data = response.json().get("data", {})
    
    # Extract key metrics
    total_market_cap = data.get("quote", {}).get("USD", {}).get("total_market_cap")
    total_volume_24h = data.get("quote", {}).get("USD", {}).get("total_volume_24h")
    btc_dominance = data.get("btc_dominance")
    
    return {
        "total_market_cap": total_market_cap,
        "total_volume_24h": total_volume_24h,
        "btc_dominance": btc_dominance
    }

def fetch_coinmarketcap_historical_data(days: int = 30) -> dict:
    """
    Fetches historical global market data from CoinMarketCap for the last `days` days.

    :param days: Number of past days to retrieve data for.
    :return: A dictionary with time-series data on market cap, volume, and BTC dominance.
    """
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")
    }

    # Define time range (from X days ago to now)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    params = {
        "time_start": start_time.isoformat(),
        "time_end": end_time.isoformat(),
        "interval": "1d"  # Fetch daily data points
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raises an error if request fails
    data = response.json().get("data", {})

    # The historical data is stored under "quotes"
    quotes = data.get("quotes", [])

    historical_metrics = []
    for entry in quotes:
        timestamp = entry.get("timestamp")  # Extract timestamp

        # Extract market metrics under "quote" > "USD"
        quote_data = entry.get("quote", {}).get("USD", {})
        market_cap = quote_data.get("total_market_cap")
        volume_24h = quote_data.get("total_volume_24h")
        btc_dominance = entry.get("btc_dominance")
        eth_dominance = entry.get("eth_dominance")  # Extra useful metric

        historical_metrics.append({
            "date": timestamp,
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "btc_dominance": btc_dominance,
            "eth_dominance": eth_dominance  # Including ETH dominance as extra insight
        })

    return {"historical_metrics": historical_metrics}

def fetch_fear_greed_index(days: int = 30) -> dict:
    """
    Fetches historical Fear & Greed Index data from CoinMarketCap for the past `days` days.

    :param days: Number of past days to retrieve the index for.
    :return: A dictionary containing the historical Fear & Greed Index values.
    """
    url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")  # Ensure API key is set
    }

    # Define time range (from X days ago to now)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    params = {
        "time_start": start_time.isoformat(),
        "time_end": end_time.isoformat(),
        "limit": days  # Limit to the requested number of days
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error if request fails
    data = response.json().get("data", [])

    # Extract relevant Fear & Greed Index values
    historical_data = []

    for entry in data:
        timestamp = entry.get("timestamp") 
        value = entry.get("value")
        classification = entry.get("value_classification")  # e.g., Extreme Fear, Greed
        date = datetime.utcfromtimestamp(int(timestamp)).strftime("%Y-%m-%d")

        historical_data.append({
            "date": date,
            "fear_greed_value": value,
            "classification": classification
        })

    return {"fear_greed_history": historical_data}

def fetch_altcoin_dominance(days: int = 30) -> dict:
    """
    Fetches historical altcoin dominance data by calculating Bitcoin dominance vs. total market cap.

    :param days: Number of past days to retrieve the data for.
    :return: A dictionary containing historical altcoin and BTC dominance trends.
    """
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")  # Ensure API key is set
    }

    # Define time range (from X days ago to now)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    params = {
        "time_start": start_time.isoformat(),
        "time_end": end_time.isoformat(),
        "interval": "1d"  # Daily intervals
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error if request fails
    data = response.json().get("data", {}).get("quotes", [])

    # Extract relevant Bitcoin & Altcoin dominance values
    historical_data = []
    for entry in data:
        timestamp = entry.get("timestamp")
        btc_dominance = entry.get("btc_dominance")
        altcoin_dominance = 100 - btc_dominance  # Altcoin dominance is 100% - BTC dominance

        # Convert timestamp from ISO format to readable date
        date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

        historical_data.append({
            "date": date,
            "btc_dominance": btc_dominance,
            "altcoin_dominance": altcoin_dominance
        })

    return {"altcoin_dominance_history": historical_data}


if __name__ == "__main__":
    data = fetch_altcoin_dominance()
    print(data)