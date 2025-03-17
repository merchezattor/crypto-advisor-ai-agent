"""
LangChain tools for cryptocurrency market analysis.

This module provides various tools for fetching and analyzing cryptocurrency market data.
"""

from langchain.tools import StructuredTool, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper

from crypto_advisor.api.chart import fetch_chart_data_tool
from crypto_advisor.api.patterns import recognize_patterns_tool
from crypto_advisor.api.technical import analyze_technical_data_tool
from crypto_advisor.api.market import (
    get_historical_market_data_tool, 
    get_altcoin_dominance_tool, 
    get_fear_greed_index_tool
)

def get_search_tool():
    """Create and return the web search tool."""
    search = GoogleSerperAPIWrapper()
    return Tool(
        name="search",
        func=search.run,
        description="Useful for retrieving current information via web search."
    )

def get_all_tools():
    """Return all configured tools for the agent."""
    return [
        get_coinmarketcap_historical_tool(),
        get_altcoin_market_tool(),
        get_binance_chart_tool(),
        get_technical_analysis_tool(),
        get_pattern_recognition_tool(),
        get_fear_greed_index_tool(),
        get_search_tool()
    ]

def get_coinmarketcap_historical_tool():
    """Create and return the CoinMarketCap historical data tool."""
    return StructuredTool.from_function(
        get_historical_market_data_tool,
        name="coinmarketcap_historical",
        description=(
            "Fetches historical global market data from CoinMarketCap for a given number of past days. "
            "This includes total market cap, 24h volume, Bitcoin dominance, and Ethereum dominance. "
            "Use this tool when analyzing long-term market trends and comparing current conditions to past cycles. "
            "Do NOT just list the data; instead, extract key insights like trends, reversals, or unusual movements."
        )
    )

def get_altcoin_market_tool():
    """Create and return the altcoin market analysis tool."""
    return StructuredTool.from_function(
        get_altcoin_dominance_tool,
        name="altcoin_market_analysis",
        description=(
            "Fetches historical Bitcoin and altcoin dominance data from CoinMarketCap for a given number of past days. "
            "This tool tracks capital flow trends—whether money is moving into Bitcoin (risk-off) or altcoins (risk-on). "
            "Use this tool to detect altcoin seasons, Bitcoin dominance surges, and potential market shifts. "
            "Do NOT just list the values—analyze the trend and explain its impact."
        )
    )

def get_binance_chart_tool():
    """Create and return the Binance chart data tool."""
    return StructuredTool.from_function(
        fetch_chart_data_tool,
        name="binance_chart_tool",
        description=(
            "Fetch OHLCV candlestick chart data for a cryptocurrency from Binance. "
            "The input should be a JSON object with the following keys: "
            "`symbol` (e.g., BTCUSDT), `interval` (e.g., 1m, 1h, 4h, 1d), and `limit` (the number of candles to fetch). "
            "Note: You can also use the alias `num_candles` for `limit`."
        )
    )

def get_technical_analysis_tool():
    """Create and return the technical analysis tool."""
    return StructuredTool.from_function(
        analyze_technical_data_tool,
        name="technical_analysis",
        description=(
            "Performs technical analysis on candlestick data, calculating indicators such as RSI, Stochastic RSI, MACD, "
            "Moving Averages (SMA, EMA), Bollinger Bands, ATR, ADX, VWAP, and On-Balance Volume. "
            "This tool provides raw indicator values without predefined insights, allowing for flexible interpretation."
        )
    )

def get_pattern_recognition_tool():
    """Create and return the pattern recognition tool."""
    return StructuredTool.from_function(
        recognize_patterns_tool,
        name="pattern_recognition",
        description=(
            "Detects key candlestick patterns from OHLCV (Open, High, Low, Close, Volume) data. "
            "The tool identifies both bullish and bearish patterns that can indicate trend reversals or continuations. "
            "It detects the following patterns: "
            "- **Doji**: Market indecision, potential reversal. "
            "- **Hammer**: Bullish reversal, occurs at the bottom of a downtrend. "
            "- **Hanging Man**: Bearish reversal, occurs at the top of an uptrend. "
            "- **Engulfing** (Bullish/Bearish): A strong reversal pattern. "
            "- **Morning Star**: Bullish reversal pattern in three candles. "
            "- **Evening Star**: Bearish reversal pattern in three candles. "
            "- **Three White Soldiers**: Strong bullish continuation signal. "
            "- **Three Black Crows**: Strong bearish continuation signal. "
            "The tool provides a structured response, indicating the detected patterns, timestamps, and signal strength. "
            "Positive values indicate a bullish pattern, while negative values indicate a bearish pattern."
            "Probability of bearish and bullish scenarios should be provided."
        )
    )

def get_fear_greed_index_tool():
    """Create and return the fear and greed index tool."""
    return StructuredTool.from_function(
        get_fear_greed_index_tool,
        name="fear_greed_index",
        description=(
            "Fetches historical Fear & Greed Index data from CoinMarketCap for a given number of past days. "
            "The index measures market sentiment on a scale from Extreme Fear to Extreme Greed. "
            "Use this tool to analyze shifts in sentiment and predict potential market reversals. "
            "Do NOT just list the values—identify patterns, major sentiment shifts, and anomalies."
        )
    ) 