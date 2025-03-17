"""
Test script for the AI agent.
This script verifies that the agent is set up correctly without making actual API calls.
"""

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Check if API keys are set
api_keys = {
    "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY'),
    "SERPER_API_KEY": os.getenv('SERPER_API_KEY')
}

print("Checking environment setup:")
for key, value in api_keys.items():
    if value:
        print(f"✅ {key} is set")
    else:
        print(f"❌ {key} is not set")

# Initialize LLM with minimal settings
try:
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=100  # Small value for testing
    )
    print("✅ LLM initialized successfully")
except Exception as e:
    print(f"❌ Error initializing LLM: {e}")

print("\nAgent setup test complete. If you see any errors above, please check your .env file and API keys.")
print("\nTo run the full agent, use: poetry run python main.py") 