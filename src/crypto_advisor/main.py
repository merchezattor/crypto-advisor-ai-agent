"""
Main entry point for the Crypto Advisor application.

This module provides functions to run the agent with predefined or custom queries.
"""

from crypto_advisor.agent import load_environment
from crypto_advisor.workflows import (
    build_market_overview_app,
    build_technical_analysis_app,
)

def run_agent(query_type="market_overview", custom_query=None, symbol: str = "ETHUSDT", days: int = 60):
    """
    Run the crypto advisor agent with the specified query.
    
    Args:
        query_type: Type of predefined query to use ('market_overview' or 'technical_analysis')
        custom_query: A custom query to run instead of a predefined one
        symbol: The symbol for the technical analysis
        days: The number of days for the market overview
        
    Returns:
        The agent's response
    """
    # Load environment variables once (inside workflow builder too, but cheap)
    load_environment()

    if custom_query is not None:
        raise NotImplementedError("Custom ad-hoc queries are not yet supported in LangGraph workflows.")

    if query_type == "technical_analysis":
        app = build_technical_analysis_app(symbol)
    else:
        app = build_market_overview_app(days)

    result = app.invoke({})
    # The graph returns a dict with the final message list.  Extract the last
    # AI message content for CLI use.
    return result["messages"][-1].content 