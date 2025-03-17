import pandas as pd
import ta
import pandas_ta as pta

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

def calculate_volatility_index(candlestick_data: list) -> dict:
    """
    Calculate a volatility index for a cryptocurrency trading pair using ATR, BBW, and HV.
    
    Args:
        candlestick_data: List of dictionaries containing OHLCV candlestick data
        
    Returns:
        Dictionary containing a volatility index from 0 (low volatility) to 5 (high volatility)
    """
    print("Calculating volatility index...")
    
    # Prepare the DataFrame
    df = pd.DataFrame(candlestick_data)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    
    # Calculate returns for historical volatility calculation
    df["returns"] = df["close"].pct_change() * 100  # percentage returns
    
    # Calculate ATR (Average True Range)
    df["ATR"] = ta.volatility.average_true_range(df["high"], df["low"], df["close"], window=14)
    
    # Calculate BBW (Bollinger Band Width)
    indicator_bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    df["Bollinger_High"] = indicator_bb.bollinger_hband()
    df["Bollinger_Low"] = indicator_bb.bollinger_lband()
    df["Bollinger_Mid"] = indicator_bb.bollinger_mavg()
    df["BBW"] = (df["Bollinger_High"] - df["Bollinger_Low"]) / df["Bollinger_Mid"]
    
    # Calculate HV (Historical Volatility) - standard deviation of returns over a period
    df["HV"] = df["returns"].rolling(window=20).std()
    
    # Get the latest values and normalize to 0-5 scale
    latest_data = df.iloc[-1]
    
    # Get the data from the last few periods to establish ranges
    recent_data = df.iloc[-30:]
    
    # Normalize each indicator to a 0-5 scale based on its recent range
    # For ATR
    atr_min = recent_data["ATR"].min()
    atr_max = recent_data["ATR"].max()
    atr_range = max(atr_max - atr_min, 0.001)  # Prevent division by zero
    atr_score = 5 * (latest_data["ATR"] - atr_min) / atr_range
    atr_score = max(0, min(5, atr_score))  # Clamp to 0-5 range
    
    # For BBW
    bbw_min = recent_data["BBW"].min()
    bbw_max = recent_data["BBW"].max()
    bbw_range = max(bbw_max - bbw_min, 0.001)  # Prevent division by zero
    bbw_score = 5 * (latest_data["BBW"] - bbw_min) / bbw_range
    bbw_score = max(0, min(5, bbw_score))  # Clamp to 0-5 range
    
    # For HV
    hv_min = recent_data["HV"].min()
    hv_max = recent_data["HV"].max()
    hv_range = max(hv_max - hv_min, 0.001)  # Prevent division by zero
    hv_score = 5 * (latest_data["HV"] - hv_min) / hv_range
    hv_score = max(0, min(5, hv_score))  # Clamp to 0-5 range
    
    # Calculate the combined volatility index as a weighted average
    # Give more weight to BBW as it tends to be a good leading indicator
    volatility_index = (atr_score * 0.3) + (bbw_score * 0.4) + (hv_score * 0.3)
    volatility_index = round(volatility_index, 1)  # Round to 1 decimal place
    
    # Create a volatility category
    if volatility_index < 1:
        volatility_category = "Very Low"
    elif volatility_index < 2:
        volatility_category = "Low"
    elif volatility_index < 3:
        volatility_category = "Moderate"
    elif volatility_index < 4:
        volatility_category = "High"
    else:
        volatility_category = "Very High"
    
    # Return the results
    return {
        "volatility_index": volatility_index,
        "volatility_category": volatility_category,
        "components": {
            "atr_score": round(atr_score, 1),
            "bbw_score": round(bbw_score, 1),
            "hv_score": round(hv_score, 1)
        },
        "raw_values": {
            "atr": latest_data["ATR"],
            "bbw": latest_data["BBW"],
            "hv": latest_data["HV"]
        }
    }

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