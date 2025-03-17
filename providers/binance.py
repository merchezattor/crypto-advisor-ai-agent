import requests
import pandas as pd
import ta
import pandas_ta as pta

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

def calculate_trend_indicators(df):
    df["SMA_50"] = ta.sma(df["close"], length=50)  # 50-period SMA
    df["EMA_20"] = ta.ema(df["close"], length=20)  # 20-period EMA
    df["ADX"] = ta.adx(df["high"], df["low"], df["close"], length=14)["ADX_14"]  # ADX Trend Strength
    return df

def calculate_momentum_indicators(df):
    df["RSI"] = ta.rsi(df["close"], length=14)  # RSI with 14 periods
    
    # Fix for Stochastic RSI: Extract specific columns
    stoch_rsi = ta.stochrsi(df["close"], length=14)
    df["Stoch_RSI_K"] = stoch_rsi["STOCHRSIk_14_14_3_3"]  # %K line
    df["Stoch_RSI_D"] = stoch_rsi["STOCHRSId_14_14_3_3"]  # %D line
    
    macd = ta.macd(df["close"])
    df["MACD"] = macd["MACD_12_26_9"]  # MACD main line
    df["MACD_Signal"] = macd["MACDs_12_26_9"]  # MACD signal line
    return df

def calculate_volatility_indicators(df):
    bbands = ta.bbands(df["close"], length=20)
    df["Bollinger_High"] = bbands["BBU_20_2.0"]  # Upper band
    df["Bollinger_Low"] = bbands["BBL_20_2.0"]  # Lower band
    df["ATR"] = ta.atr(df["high"], df["low"], df["close"], length=14)  # ATR for volatility
    return df

def calculate_volume_indicators(df):
    df["OBV"] = ta.obv(df["close"], df["volume"])  # On-Balance Volume
    df["CMF"] = ta.cmf(df["high"], df["low"], df["close"], df["volume"], length=20)  # Chaikin Money Flow
    df["VWAP"] = ta.vwap(df["high"], df["low"], df["close"], df["volume"])  # VWAP Indicator
    return df

def perform_technical_analysis(candlestick_data: list) -> dict:
    print("Performing technical analysis...")
    
    df = pd.DataFrame(candlestick_data)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    
    df = calculate_trend_indicators(df)
    df = calculate_momentum_indicators(df)
    df = calculate_volatility_indicators(df)
    df = calculate_volume_indicators(df)
    
    latest_data = df.iloc[-1].to_dict()
    
    return {
        "latest_indicators": latest_data
    }

def detect_selected_patterns(candlestick_data: list) -> pd.DataFrame:
    """
    Detects selected candlestick patterns in the given OHLCV data.

    :param candlestick_data: List of dictionaries with keys ['time', 'open', 'high', 'low', 'close', 'volume']
    :return: DataFrame with new columns for each detected pattern.
    """
    df = pd.DataFrame(candlestick_data)
    df['time'] = pd.to_datetime(df['time'])

    df.set_index('time', inplace=True)

    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    selected_patterns = [
        'doji',
        'hammer',
        'hangingman',
        'engulfing',
        'morningstar',
        'eveningstar',
        '3whitesoldiers',
        '3blackcrows'
    ]


    pattern_map = {}
    
    # print(pattern_df)

    for pattern in selected_patterns:

        pattern_df = ta.cdl_pattern(
            open_=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name=pattern
        )

        if pattern_df is not None and not pattern_df.empty:
            df = pd.concat([df, pattern_df], axis=1)
            actual_column_name = pattern_df.columns[0]
            pattern_map[pattern] = actual_column_name

    pattern_signals = {}

    for pattern, column_name in pattern_map.items():
        if column_name in df.columns:
            detected = df[column_name].iloc[-3:].replace(0, None).dropna().to_dict()
            if detected:
                pattern_signals[pattern] = detected

    return {"detected_patterns": pattern_signals}

if __name__ == "__main__":
    symbol = "ETHUSDT"
    interval = "1h"
    limit = 100

    data = fetch_binance_chart(symbol, interval, limit)
    ta_data = perform_technical_analysis(data)

    print('Technical Analysis done')

    pattern_data = detect_selected_patterns(data)

    print(pattern_data)