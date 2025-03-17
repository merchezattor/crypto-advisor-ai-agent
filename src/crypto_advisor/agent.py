"""
Agent initialization and configuration.

This module sets up the LangChain agent with the appropriate tools and configuration.
"""

import os
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from crypto_advisor.tools import get_all_tools

def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    
    # Set environment variables for services
    os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
    os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')

def create_llm():
    """Create and configure the language model."""
    return ChatOpenAI(
        model="o3-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

def create_agent():
    """Create and configure the LangChain agent."""
    # Initialize the LLM
    llm = create_llm()
    
    # Get all tools
    tools = get_all_tools()
    
    # Initialize the agent
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
    
    return agent 