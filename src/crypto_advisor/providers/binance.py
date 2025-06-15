"""Binance API provider.

This module provides functions for fetching candlestick data from the Binance
API using the `python-binance` library.
"""

from datetime import datetime

from binance.client import Client
from binance.exceptions import BinanceAPIException


client = Client(ping=False)

def fetch_binance_chart(symbol: str, interval: str = "1h", limit: int = 50):
    """Fetch candlestick data from Binance using `python-binance`.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
        interval: Candlestick interval (e.g., '1h', '4h', '1d')
        limit: Number of candles to fetch
        
    Returns:
        List of dictionaries containing candlestick data
    """
    print("Fetching Binance chart data...")

    try:
        data = client.get_klines(
            symbol=symbol.upper(),
            interval=interval,
            limit=limit,
        )
    except BinanceAPIException as exc:
        raise RuntimeError(f"Failed to fetch data from Binance: {exc}") from exc
    
    candles = [
        {
            "time": datetime.fromtimestamp(int(candle[0]) / 1000),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
        }
        for candle in data
    ]

    print("Candles processed successfully!")
    
    return candles

