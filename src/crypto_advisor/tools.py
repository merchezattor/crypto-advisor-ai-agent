"""
LangChain tools for cryptocurrency market analysis.

This module provides various tools for fetching and analyzing cryptocurrency market data.
"""

from langchain.tools import StructuredTool, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper

from crypto_advisor.api.chart import fetch_chart_data_tool
from crypto_advisor.api.patterns import recognize_patterns_tool
from crypto_advisor.api.technical import analyze_technical_data_tool

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
        get_fear_greed_structured_tool(),
        get_volatility_index_tool(),
        get_search_tool()
    ]

def get_coinmarketcap_historical_tool():
    """Return historical market data tool accepting simple ``days`` param."""

    def _hist(days: int = 30):  # noqa: WPS110
        from crypto_advisor.api.market import get_historical_market_data_tool

        from crypto_advisor.api.models.market import HistoricalMarketDataRequest

        return get_historical_market_data_tool(HistoricalMarketDataRequest(days=days))

    return StructuredTool.from_function(
        _hist,
        name="coinmarketcap_historical",
        description=(
            "Fetch historical global market data from CoinMarketCap. Accepts `days` (int)."
        ),
    )

def get_altcoin_market_tool():
    """Return altcoin dominance tool with simple ``days`` param."""

    def _dom(days: int = 30):
        from crypto_advisor.api.market import get_altcoin_dominance_tool
        from crypto_advisor.api.models.market import AltcoinDominanceRequest

        return get_altcoin_dominance_tool(AltcoinDominanceRequest(days=days))

    return StructuredTool.from_function(
        _dom,
        name="altcoin_market_analysis",
        description="Fetch Bitcoin vs altcoin dominance data. Accepts `days` (int).",
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

def get_volatility_index_tool():
    """Return the volatility index tool with a simple list parameter."""

    from typing import List, Dict
    from crypto_advisor.api.volatility import analyze_volatility_tool
    from crypto_advisor.api.models.technical import TechnicalAnalysisRequest

    def _volatility(candlestick_data: List[Dict]):  # type: ignore[valid-type]
        """Wrapper forwarding raw candle data to the analyzer."""

        req = TechnicalAnalysisRequest(candlestick_data=candlestick_data)
        return analyze_volatility_tool(req)

    return StructuredTool.from_function(
        _volatility,
        name="volatility_index",
        description=(
            "Calculates a volatility index (0-5) from candlestick data using ATR, BBW, and HV. "
            "Returns the index value, category label, and component scores."
        ),
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

def get_fear_greed_structured_tool():
    """Return Fear & Greed Index tool as a StructuredTool."""

    def _fg(days: int = 30):
        from crypto_advisor.api.market import get_fear_greed_index_tool
        from crypto_advisor.api.models.market import FearGreedIndexRequest

        return get_fear_greed_index_tool(FearGreedIndexRequest(days=days))

    return StructuredTool.from_function(
        _fg,
        name="fear_greed_index",
        description="Fetch Fear & Greed Index data. Accepts `days` (int).",
    ) 