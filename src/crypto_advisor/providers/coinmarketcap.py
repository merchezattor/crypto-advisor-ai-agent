"""
CoinMarketCap API provider.

This module provides functions for fetching data from the CoinMarketCap API.
"""

import os
import requests
from datetime import datetime, timedelta

from dotenv import load_dotenv

def fetch_coinmarketcap_global_data() -> dict:
    """
    Fetches global market data from CoinMarketCap.
    
    Returns:
        Dictionary with total market cap, 24h volume, and BTC dominance.
    """
    print("Fetching global market data from CoinMarketCap...")
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    return {
        "total_market_cap": data["data"]["quote"]["USD"]["total_market_cap"],
        "total_volume_24h": data["data"]["quote"]["USD"]["total_volume_24h"],
        "btc_dominance": data["data"]["btc_dominance"],
        "eth_dominance": data["data"]["eth_dominance"],
        "timestamp": data["status"]["timestamp"]
    }

def fetch_coinmarketcap_historical_data(days: int = 30) -> dict:
    """
    Fetches historical global market data from CoinMarketCap.
    
    Args:
        days: Number of days of historical data to fetch
        
    Returns:
        Dictionary containing historical market data
    """
    print("Fetching historical CoinMarketCap data...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical"
    
    params = {
        "time_start": start_date.isoformat(),
        "time_end": end_date.isoformat(),
        "interval": "1d"  # daily data
    }
    
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raises an error if request fails
    data = response.json()
    
    historical_data = []
    for quote in data["data"]["quotes"]:
        historical_data.append({
            "timestamp": quote["timestamp"],
            "total_market_cap": quote["quote"]["USD"]["total_market_cap"],
            "total_volume_24h": quote["quote"]["USD"]["total_volume_24h"],
            "btc_dominance": quote["btc_dominance"],
            "eth_dominance": quote["eth_dominance"]
        })
    
    # Process the data to calculate trends
    market_cap_change = calculate_percent_change(
        historical_data[0]["total_market_cap"], 
        historical_data[-1]["total_market_cap"]
    )
    
    volume_change = calculate_percent_change(
        historical_data[0]["total_volume_24h"], 
        historical_data[-1]["total_volume_24h"]
    )
    
    btc_dominance_change = historical_data[-1]["btc_dominance"] - historical_data[0]["btc_dominance"]
    
    return {
        "historical_data": historical_data,
        "summary": {
            "market_cap_change_percent": market_cap_change,
            "volume_change_percent": volume_change,
            "btc_dominance_change": btc_dominance_change,
            "period_days": days
        }
    }

def fetch_fear_greed_index(days: int = 30) -> dict:
    """
    Fetches historical Fear and Greed Index data.
    
    Args:
        days: Number of days of historical data to fetch
        
    Returns:
        Dictionary containing fear and greed index data
    """
    print("Fetching Fear & Greed Index data...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    url = "https://api.alternative.me/fng/"
    
    params = {
        "limit": days,
        "format": "json",
        "date_format": "world"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    fear_greed_data = []
    for item in data["data"]:
        fear_greed_data.append({
            "value": int(item["value"]),
            "value_classification": item["value_classification"],
            "timestamp": item["timestamp"],
            "time_until_update": item["time_until_update"]
        })
    
    # Sort by timestamp (most recent first)
    fear_greed_data.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Calculate trends and current state
    current_value = fear_greed_data[0]["value"]
    current_classification = fear_greed_data[0]["value_classification"]
    
    avg_value = sum(item["value"] for item in fear_greed_data) / len(fear_greed_data)
    
    # Determine if sentiment is improving or worsening
    sentiment_trend = "neutral"
    if len(fear_greed_data) > 7:
        week_avg = sum(item["value"] for item in fear_greed_data[:7]) / 7
        month_avg = avg_value
        
        if week_avg > month_avg + 5:
            sentiment_trend = "improving"
        elif week_avg < month_avg - 5:
            sentiment_trend = "worsening"
    
    return {
        "current": {
            "value": current_value,
            "classification": current_classification
        },
        "historical": fear_greed_data,
        "analysis": {
            "average_value": avg_value,
            "sentiment_trend": sentiment_trend,
            "period_days": days
        }
    }

def fetch_altcoin_dominance(days: int = 30) -> dict:
    """
    Calculates and returns historical Bitcoin dominance vs altcoin dominance.
    
    Args:
        days: Number of days of historical data to fetch
        
    Returns:
        Dictionary containing Bitcoin and altcoin dominance data
    """
    print("Calculating Bitcoin vs Altcoin dominance...")
    
    # We'll get this data from the historical global metrics
    historical_data = fetch_coinmarketcap_historical_data(days)["historical_data"]
    
    dominance_data = []
    for day_data in historical_data:
        btc_dom = day_data["btc_dominance"]
        eth_dom = day_data["eth_dominance"]
        altcoin_dom = 100 - btc_dom  # All non-BTC coins
        other_dom = 100 - btc_dom - eth_dom  # All non-BTC, non-ETH coins
        
        dominance_data.append({
            "timestamp": day_data["timestamp"],
            "btc_dominance": btc_dom,
            "eth_dominance": eth_dom,
            "altcoin_dominance": altcoin_dom,
            "other_dominance": other_dom
        })
    
    # Sort by timestamp (oldest first for trend analysis)
    dominance_data.sort(key=lambda x: x["timestamp"])
    
    # Analysis of capital flow trends
    btc_dom_change = dominance_data[-1]["btc_dominance"] - dominance_data[0]["btc_dominance"]
    altcoin_dom_change = dominance_data[-1]["altcoin_dominance"] - dominance_data[0]["altcoin_dominance"]
    eth_dom_change = dominance_data[-1]["eth_dominance"] - dominance_data[0]["eth_dominance"]
    
    # Current state
    current_state = dominance_data[-1]
    
    return {
        "current": current_state,
        "historical": dominance_data,
        "analysis": {
            "btc_dominance_change": btc_dom_change,
            "altcoin_dominance_change": altcoin_dom_change,
            "eth_dominance_change": eth_dom_change,
            "capital_flow": "Into Bitcoin" if btc_dom_change > 0 else "Into Altcoins",
            "period_days": days
        }
    }

def calculate_percent_change(start_value, end_value):
    """Helper function to calculate percent change between two values."""
    if start_value == 0:
        return 0
    return ((end_value - start_value) / start_value) * 100 