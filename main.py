import os
import tools

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

os.environ["OPEN_AI_API_KEY"] = os.getenv('OPEN_AI_API_KEY')
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
    tools.altcoin_market_tool
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
    "Analyze Bitcoin's market situation, including historical trends from the last 60 days. "
    "Focus on significant changes, anomalies, or patterns in market cap, volume, and dominance. "
    "Identify whether we are seeing signs of accumulation, distribution, or a potential reversal. "
    "Identify key sentiment shifts, periods of extreme greed or fear, and how they correlate with Bitcoin price movements."
    "Identify whether capital is flowing into BTC or altcoins, and explain any major shifts. "
    "Do NOT just repeat numbers—provide clear insights backed by data.")
]

response = agent.invoke(messages)