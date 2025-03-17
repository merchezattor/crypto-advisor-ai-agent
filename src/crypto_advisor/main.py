"""
Main entry point for the Crypto Advisor application.

This module provides functions to run the agent with predefined or custom queries.
"""

from crypto_advisor.agent import load_environment, create_agent

def market_overview_query():
    """Return a query for getting a global market overview."""
    return [
        ("human", 
        "Provide a global market overview for today, using historical trends from the last 60 days as context. "
        "Summarize the current state of the crypto market, including total market cap trends, Bitcoin dominance shifts, and key volume movements. "
        "Assess the Fear & Greed Index and explain whether the sentiment aligns with price action. "
        "Identify any major anomalies or unusual market behavior in the last few days. "
        "Evaluate whether capital is flowing into BTC or altcoins and describe the implications. "
        "Summarize potential scenarios for the market in the short term (bullish, bearish, or uncertain) based on current data. "
        "Do NOT just repeat numbers—provide clear, investor-focused insights backed by data.")
    ]

def technical_analysis_query():
    """Return a query for performing technical analysis on ETHUSDT."""
    return [
        ("human", 
        "Fetch the last 100 4-hour candlesticks for ETHUSDT. "
        "Perform a full technical analysis, including RSI, MACD, Moving Averages, Bollinger Bands, and Volume-based indicators. "
        "Additionally, detect any potential chart patterns such as Double Top, Head and Shoulders, Cup and Handle, or Triangles. "
        "Do NOT just list the values—analyze how these indicators interact and what they signal together. "
        "If conflicting signals appear, explain which indicator is more reliable in the current market. "
        "Summarize whether BTC is currently in a bullish, bearish, or uncertain phase based on the combined results. "
        "Provide a short-term market outlook, highlighting key levels to watch for breakouts or reversals."
        "Also give probability of bullish and bearish scenarios."
        )
    ]

def run_agent(query_type="market_overview", custom_query=None):
    """
    Run the crypto advisor agent with the specified query.
    
    Args:
        query_type: Type of predefined query to use ('market_overview' or 'technical_analysis')
        custom_query: A custom query to run instead of a predefined one
        
    Returns:
        The agent's response
    """
    # Load environment variables
    load_environment()
    
    # Create the agent
    agent = create_agent()
    
    # Get the query
    if custom_query:
        messages = [("human", custom_query)]
    elif query_type == "technical_analysis":
        messages = technical_analysis_query()
    else:
        messages = market_overview_query()
    
    # Run the agent
    response = agent.invoke(messages)
    return response

if __name__ == "__main__":
    run_agent() 