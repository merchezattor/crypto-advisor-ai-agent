from api_requests.chart_request import fetch_chart_data_tool
from langchain.tools import StructuredTool

from langchain.agents import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper

from providers.binance import identify_patterns, perform_technical_analysis
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
        "Performs technical analysis on candlestick data, calculating indicators such as RSI, MACD, Moving Averages, "
        "Bollinger Bands, and On-Balance Volume. "
        "It identifies overbought/oversold conditions, trend momentum, and potential reversals. "
        "Use this tool to analyze price action and generate trading insights."
    )
)

pattern_recognition_tool = StructuredTool.from_function(
    identify_patterns,
    name="pattern_recognition",
    description=(
        "Detects technical chart patterns from historical candlestick data, including Double Top, Double Bottom, "
        "Head and Shoulders, Inverse Head and Shoulders, Triangles, Flags, Wedges, Cup and Handle, "
        "Triple Top, Triple Bottom, Diamond Patterns, and Rectangle Consolidation. "
        "Use this tool to identify potential market reversals and breakout setups."
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