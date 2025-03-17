import os
import tools

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

tools = [
    tools.web_search_tool,
    tools.technical_analysis_tool,
    tools.binance_chart_tool,
    tools.coinmarketcap_historical_tool,
    tools.fear_greed_index_tool,
    tools.altcoin_market_tool,
    tools.technical_analysis_tool,
    tools.pattern_recognition_tool
]

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=True,
    handle_parsing_errors=True,
    system_message=(
        "You are an advanced financial analysis assistant specializing in cryptocurrency markets. "
        "Your goal is to analyze market data across different timeframes, identifying trends, anomalies, "
        "and key indicators that provide actionable insights. "
        "Do NOT just repeat raw data—always interpret the meaning behind the data. "
        "Focus on what has changed, why it matters, and how it might affect the market."
        "Give recommendations based on the analysis and provide clear reasoning for your conclusions."
    )
)

messages = [
    ("human", 
    "Provide a global market overview for today, using historical trends from the last 60 days as context. "
    "Summarize the current state of the crypto market, including total market cap trends, Bitcoin dominance shifts, and key volume movements. "
    "Assess the Fear & Greed Index and explain whether the sentiment aligns with price action. "
    "Identify any major anomalies or unusual market behavior in the last few days. "
    "Evaluate whether capital is flowing into BTC or altcoins and describe the implications. "
    "Summarize potential scenarios for the market in the short term (bullish, bearish, or uncertain) based on current data. "
    "Do NOT just repeat numbers—provide clear, investor-focused insights backed by data.")
]

# ## technical analysis
# messages = [
#     ("human", 
#     "Fetch the last 100 4-hour candlesticks for ETHUSDT. "
#     "Perform a full technical analysis, including RSI, MACD, Moving Averages, Bollinger Bands, and Volume-based indicators. "
#     "Additionally, detect any potential chart patterns such as Double Top, Head and Shoulders, Cup and Handle, or Triangles. "
#     "Do NOT just list the values—analyze how these indicators interact and what they signal together. "
#     "If conflicting signals appear, explain which indicator is more reliable in the current market. "
#     "Summarize whether BTC is currently in a bullish, bearish, or uncertain phase based on the combined results. "
#     "Provide a short-term market outlook, highlighting key levels to watch for breakouts or reversals."
#     "Also give probability of bullish and bearhish scenarios."
#     )
# ]

response = agent.invoke(messages)