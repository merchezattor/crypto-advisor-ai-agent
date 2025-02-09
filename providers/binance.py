import requests
import pandas as pd
import numpy as np
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

def perform_technical_analysis(candlestick_data: list) -> dict:
    """
    Performs technical analysis on candlestick data.

    :param candlestick_data: List of OHLCV (Open, High, Low, Close, Volume) data.
    :return: Dictionary with computed indicators and insights.
    """
    print("Performing technical analysis...")
    # Convert list to DataFrame
    df = pd.DataFrame(candlestick_data)

    # Ensure correct data types
    df["time"] = pd.to_datetime(df["time"])  # Convert time column to datetime
    df.set_index("time", inplace=True)  # Set time as index
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    # 🟢 1️⃣ TREND INDICATORS
    df["SMA_50"] = ta.trend.sma_indicator(df["close"], window=50)  # 50-period SMA
    df["EMA_20"] = ta.trend.ema_indicator(df["close"], window=20)  # 20-period EMA

    # 🟡 2️⃣ MOMENTUM INDICATORS
    df["RSI"] = ta.momentum.rsi(df["close"], window=14)  # RSI with 14 periods
    df["MACD"] = ta.trend.macd(df["close"])  # MACD main line
    df["MACD_Signal"] = ta.trend.macd_signal(df["close"])  # MACD signal line

    # 🔴 3️⃣ VOLATILITY INDICATORS
    df["Bollinger_High"] = ta.volatility.bollinger_hband(df["close"], window=20)  # Upper band
    df["Bollinger_Low"] = ta.volatility.bollinger_lband(df["close"], window=20)  # Lower band

    # 🔵 4️⃣ VOLUME INDICATORS
    df["OBV"] = ta.volume.on_balance_volume(df["close"], df["volume"])  # On-Balance Volume

    # Select relevant columns for output
    latest_data = df.iloc[-1].to_dict()

    # Interpret key signals
    insights = []

    # RSI Interpretation
    if latest_data["RSI"] > 70:
        insights.append("RSI is above 70, indicating overbought conditions (possible correction).")
    elif latest_data["RSI"] < 30:
        insights.append("RSI is below 30, indicating oversold conditions (possible rebound).")

    # MACD Interpretation
    if latest_data["MACD"] > latest_data["MACD_Signal"]:
        insights.append("MACD line is above Signal line, suggesting bullish momentum.")
    else:
        insights.append("MACD line is below Signal line, suggesting bearish momentum.")

    # Bollinger Bands Interpretation
    if latest_data["close"] >= latest_data["Bollinger_High"]:
        insights.append("Price is near the upper Bollinger Band, indicating potential overbought conditions.")
    elif latest_data["close"] <= latest_data["Bollinger_Low"]:
        insights.append("Price is near the lower Bollinger Band, indicating potential oversold conditions.")

    return {
        "latest_indicators": latest_data,
        "insights": insights
    }

def identify_patterns(candlestick_data: list) -> dict:
    """
    Identifies key chart patterns from historical candlestick data.

    :param candlestick_data: List of OHLCV (Open, High, Low, Close, Volume) data.
    :return: Dictionary with recognized chart patterns.
    """
    print("Identifying chart patterns...")
    # Convert list to DataFrame
    df = pd.DataFrame(candlestick_data)

    # Ensure correct data types
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    # Detect patterns
    recognized_patterns = []

    ### 🟢 1️⃣ DOUBLE TOP & DOUBLE BOTTOM
    if len(df) >= 5:
        recent_highs = df["high"].rolling(window=5).max()
        recent_lows = df["low"].rolling(window=5).min()

        if df["high"].iloc[-1] < recent_highs.iloc[-2] and df["high"].iloc[-3] < recent_highs.iloc[-2]:
            recognized_patterns.append("Double Top detected – Possible bearish reversal.")

        if df["low"].iloc[-1] > recent_lows.iloc[-2] and df["low"].iloc[-3] > recent_lows.iloc[-2]:
            recognized_patterns.append("Double Bottom detected – Possible bullish reversal.")

    ### 🟡 2️⃣ HEAD AND SHOULDERS (Bearish) & INVERSE HEAD AND SHOULDERS (Bullish)
    if len(df) >= 7:
        left_shoulder = df["high"].iloc[-7]
        head = df["high"].iloc[-5]
        right_shoulder = df["high"].iloc[-3]

        if left_shoulder < head and right_shoulder < head:
            recognized_patterns.append("Head and Shoulders detected – Possible bearish reversal.")

        left_shoulder = df["low"].iloc[-7]
        head = df["low"].iloc[-5]
        right_shoulder = df["low"].iloc[-3]

        if left_shoulder > head and right_shoulder > head:
            recognized_patterns.append("Inverse Head and Shoulders detected – Possible bullish breakout.")

    ### 🔴 3️⃣ TRIANGLES & WEDGE PATTERNS
    if len(df) >= 10:
        recent_highs = df["high"].rolling(window=10).max()
        recent_lows = df["low"].rolling(window=10).min()

        if np.all(np.diff(recent_highs) < 0) and np.all(np.diff(recent_lows) > 0):
            recognized_patterns.append("Symmetrical Triangle detected – Potential breakout approaching.")

        if np.all(np.diff(recent_highs) == 0) and np.all(np.diff(recent_lows) > 0):
            recognized_patterns.append("Ascending Triangle detected – Potential bullish breakout.")

        if np.all(np.diff(recent_highs) < 0) and np.all(np.diff(recent_lows) == 0):
            recognized_patterns.append("Descending Triangle detected – Potential bearish breakdown.")

    ### 🟣 4️⃣ FLAGS & PENNANTS
    if len(df) >= 10:
        recent_trend = df["close"].iloc[-10:].pct_change().sum()
        pullback = df["close"].iloc[-5:].pct_change().sum()

        if recent_trend > 0 and pullback < 0:
            recognized_patterns.append("Bullish Flag detected – Possible continuation of uptrend.")

        if recent_trend < 0 and pullback > 0:
            recognized_patterns.append("Bearish Flag detected – Possible continuation of downtrend.")

    ### 🏆 5️⃣ CUP & HANDLE
    if len(df) >= 15:
        cup_low = df["low"].rolling(window=10).min().iloc[-5]
        handle_high = df["high"].rolling(window=5).max().iloc[-1]

        if handle_high > cup_low * 1.05:  # Handle should be slightly above cup
            recognized_patterns.append("Cup and Handle detected – Potential bullish breakout.")

    ### 🔶 6️⃣ TRIPLE TOP / TRIPLE BOTTOM
    if len(df) >= 7:
        top_1 = df["high"].iloc[-7]
        top_2 = df["high"].iloc[-5]
        top_3 = df["high"].iloc[-3]

        if abs(top_1 - top_2) < 0.5 and abs(top_2 - top_3) < 0.5:
            recognized_patterns.append("Triple Top detected – Strong bearish reversal signal.")

        bot_1 = df["low"].iloc[-7]
        bot_2 = df["low"].iloc[-5]
        bot_3 = df["low"].iloc[-3]

        if abs(bot_1 - bot_2) < 0.5 and abs(bot_2 - bot_3) < 0.5:
            recognized_patterns.append("Triple Bottom detected – Strong bullish reversal signal.")

    ### 💎 7️⃣ DIAMOND TOP / BOTTOM
    if len(df) >= 12:
        max_high = df["high"].rolling(window=12).max().iloc[-1]
        min_low = df["low"].rolling(window=12).min().iloc[-1]

        if df["close"].iloc[-1] < min_low * 1.02:
            recognized_patterns.append("Diamond Top detected – Possible strong bearish reversal.")

        if df["close"].iloc[-1] > max_high * 0.98:
            recognized_patterns.append("Diamond Bottom detected – Possible strong bullish reversal.")

    ### 📏 8️⃣ RECTANGLES (Bullish & Bearish Consolidation)
    if len(df) >= 15:
        max_range = df["high"].rolling(window=15).max()
        min_range = df["low"].rolling(window=15).min()

        if np.all(np.diff(max_range) == 0) and np.all(np.diff(min_range) == 0):
            recognized_patterns.append("Rectangle pattern detected – Market consolidation.")

    return {"recognized_patterns": recognized_patterns}

if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "4h"
    limit = 100

    data = fetch_binance_chart(symbol, interval, limit)
    print(identify_patterns(data))