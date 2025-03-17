"""
Binance API provider.

This module provides functions for fetching and analyzing data from the Binance API.
"""

import requests
from datetime import datetime

def fetch_binance_chart(symbol: str, interval: str = "1h", limit: int = 50):
    """
    Fetch candlestick data from Binance API.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
        interval: Candlestick interval (e.g., '1h', '4h', '1d')
        limit: Number of candles to fetch
        
    Returns:
        List of dictionaries containing candlestick data
    """
    print("Fetching Binance chart data...")

    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    candles = [
        {
            "time": datetime.fromtimestamp(int(candle[0]) / 1000),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5])
        }
        for candle in data
    ]

    print("Candles processed successfully!")
    
    return candles

