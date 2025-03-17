import pandas as pd
import ta
import pandas_ta as pta
from datetime import datetime

def calculate_trend_indicators(df):
    """Calculate trend indicators for a DataFrame of candlestick data."""
    df["SMA_50"] = ta.trend.sma_indicator(df["close"], window=50)  # 50-period SMA
    df["EMA_20"] = ta.trend.ema_indicator(df["close"], window=20)  # 20-period EMA
    df["ADX"] = ta.trend.adx(df["high"], df["low"], df["close"], window=14)  # ADX Trend Strength
    return df

def calculate_momentum_indicators(df):
    """Calculate momentum indicators for a DataFrame of candlestick data."""
    df["RSI"] = ta.momentum.rsi(df["close"], window=14)  # RSI with 14 periods
    
    # Fix for Stochastic RSI: Extract specific columns
    stoch_rsi = pta.stochrsi(df["close"], length=14)
    df["Stoch_RSI_K"] = stoch_rsi["STOCHRSIk_14_14_3_3"]  # %K line
    df["Stoch_RSI_D"] = stoch_rsi["STOCHRSId_14_14_3_3"]  # %D line
    
    macd = ta.trend.macd(df["close"])
    df["MACD"] = macd  # MACD main line
    df["MACD_Signal"] = ta.trend.macd_signal(df["close"])  # MACD signal line
    return df

def calculate_volatility_indicators(df):
    """Calculate volatility indicators for a DataFrame of candlestick data."""
    indicator_bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    df["Bollinger_High"] = indicator_bb.bollinger_hband()  # Upper band
    df["Bollinger_Low"] = indicator_bb.bollinger_lband()  # Lower band
    df["ATR"] = ta.volatility.average_true_range(df["high"], df["low"], df["close"], window=14)  # ATR for volatility
    return df

def calculate_volume_indicators(df):
    """Calculate volume indicators for a DataFrame of candlestick data."""
    df["OBV"] = ta.volume.on_balance_volume(df["close"], df["volume"])  # On-Balance Volume
    df["CMF"] = ta.volume.chaikin_money_flow(df["high"], df["low"], df["close"], df["volume"], window=20)  # Chaikin Money Flow
    df["VWAP"] = pta.vwap(df["high"], df["low"], df["close"], df["volume"])  # VWAP Indicator
    return df

def perform_technical_analysis(candlestick_data: list) -> dict:
    """
    Perform technical analysis on candlestick data.
    
    Args:
        candlestick_data: List of dictionaries containing candlestick data
        
    Returns:
        Dictionary containing technical analysis results
    """
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

def detect_selected_patterns(candlestick_data: list) -> dict:
    """
    Detect selected candlestick patterns in the given OHLCV data.

    Args:
        candlestick_data: List of dictionaries with keys ['time', 'open', 'high', 'low', 'close', 'volume']
        
    Returns:
        Dictionary containing detected patterns
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
    
    for pattern in selected_patterns:
        pattern_df = pta.cdl_pattern(
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