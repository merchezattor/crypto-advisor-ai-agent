import requests
import pandas as pd
import ta

from datetime import datetime

def fetch_binance_chart(symbol: str, interval: str = "1h", limit: int = 50):

    print("Fetching Binance chart data...")

    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    print("Data fetched successfully!")
    
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

def analyze_binance_data(symbol: str, interval: str, limit: int) -> str:
    candles = fetch_binance_chart(symbol, interval, limit)
    if not candles:
        return "No data fetched."
    
    # Convert the list of candles into a DataFrame
    df = pd.DataFrame(candles)
    
    # Convert numeric fields to numbers
    df['open'] = pd.to_numeric(df['open'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    
    # Set the datetime index (assuming the 'time' field is already in datetime format)
    df.set_index("time", inplace=True)
    
    # Calculate RSI using the ta library (window of 14 periods)
    rsi_indicator = ta.momentum.RSIIndicator(close=df['close'], window=14)
    df['RSI'] = rsi_indicator.rsi()
    
    # Calculate Simple Moving Averages (SMA) over 20 and 50 periods
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    
    # Use the latest available candle for the analysis
    latest = df.iloc[-1]
    trend = "uptrend" if latest['SMA_20'] > latest['SMA_50'] else "downtrend"
    rsi_value = latest['RSI']
    
    return f"Analysis: The RSI is {rsi_value:.2f}. The current trend appears to be {trend}."