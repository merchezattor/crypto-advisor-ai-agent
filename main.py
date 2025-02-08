import os

from langchain.agents import initialize_agent
from langchain.agents import AgentType

from langchain_openai import ChatOpenAI

from tools import binance_chart_tool, web_search_tool, technical_analysis_tool, coinmarketcap_historical_tool

# Set API keys
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
    # web_search_tool,
    technical_analysis_tool,
    binance_chart_tool,
    coinmarketcap_historical_tool
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
    )
)

messages = [
    ("human", 
    "Analyze Bitcoin's market situation, including historical trends from the last 60 days. "
    "Focus on significant changes, anomalies, or patterns in market cap, volume, and dominance. "
    "Identify whether we are seeing signs of accumulation, distribution, or a potential reversal. "
    "Do NOT just repeat numbers—provide clear insights backed by data.")
]

response = agent.invoke(messages)