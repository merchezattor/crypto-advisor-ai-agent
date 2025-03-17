from api_requests.chart_request import fetch_chart_data_tool
from langchain.tools import StructuredTool

from langchain.agents import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper

from providers.binance import detect_selected_patterns, perform_technical_analysis
from providers.coinmarketcup import fetch_altcoin_dominance, fetch_coinmarketcap_historical_data, fetch_fear_greed_index

search = GoogleSerperAPIWrapper()

coinmarketcap_historical_tool = StructuredTool.from_function(
    fetch_coinmarketcap_historical_data,
    name="coinmarketcap_historical",
    description=(
        "Fetches historical global market data from CoinMarketCap for a given number of past days. "
        "This includes total market cap, 24h volume, Bitcoin dominance, and Ethereum dominance. "
        "Use this tool when analyzing long-term market trends and comparing current conditions to past cycles. "
        "Do NOT just list the data; instead, extract key insights like trends, reversals, or unusual movements."
    )
)

altcoin_market_tool = StructuredTool.from_function(
    fetch_altcoin_dominance,
    name="altcoin_market_analysis",
    description=(
        "Fetches historical Bitcoin and altcoin dominance data from CoinMarketCap for a given number of past days. "
        "This tool tracks capital flow trends—whether money is moving into Bitcoin (risk-off) or altcoins (risk-on). "
        "Use this tool to detect altcoin seasons, Bitcoin dominance surges, and potential market shifts. "
        "Do NOT just list the values—analyze the trend and explain its impact."
    )
)

binance_chart_tool = StructuredTool.from_function(
    fetch_chart_data_tool,
    name="binance_chart_tool",
    description=(
        "Fetch OHLCV candlestick chart data for a cryptocurrency from Binance. "
        "The input should be a JSON object with the following keys: "
        "`symbol` (e.g., BTCUSDT), `interval` (e.g., 1m, 1h, 4h, 1d), and `limit` (the number of candles to fetch). "
        "Note: You can also use the alias `num_candles` for `limit`."
    )
)

technical_analysis_tool = StructuredTool.from_function(
    perform_technical_analysis,
    name="technical_analysis",
    description=(
        "Performs technical analysis on candlestick data, calculating indicators such as RSI, Stochastic RSI, MACD, "
        "Moving Averages (SMA, EMA), Bollinger Bands, ATR, ADX, VWAP, and On-Balance Volume. "
        "This tool provides raw indicator values without predefined insights, allowing for flexible interpretation."
    )
)

pattern_recognition_tool = StructuredTool.from_function(
    detect_selected_patterns,
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
        "Probabily of bearish and bullish scenarios should be provided."
    )
)

fear_greed_index_tool = StructuredTool.from_function(
    fetch_fear_greed_index,
    name="fear_greed_index",
    description=(
        "Fetches historical Fear & Greed Index data from CoinMarketCap for a given number of past days. "
        "The index measures market sentiment on a scale from Extreme Fear to Extreme Greed. "
        "Use this tool to analyze shifts in sentiment and predict potential market reversals. "
        "Do NOT just list the values—identify patterns, major sentiment shifts, and anomalies."
    )
)

web_search_tool = Tool(
        name="search",
        func=search.run,
        description="Useful for retrieving current information via web search."
    )