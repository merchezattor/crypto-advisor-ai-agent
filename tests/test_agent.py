"""
Test script for the AI agent.

This script verifies that the agent is set up correctly without making actual API calls.
"""

import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

def test_environment_setup():
    """Test that required environment variables are set."""
    # Load environment variables
    load_dotenv()

    # Check if API keys are set
    api_keys = {
        "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY'),
        "SERPER_API_KEY": os.getenv('SERPER_API_KEY')
    }

    print("Checking environment setup:")
    all_keys_set = True
    for key, value in api_keys.items():
        if value:
            print(f"✅ {key} is set")
        else:
            print(f"❌ {key} is not set")
            all_keys_set = False
            
    return all_keys_set

def test_llm_initialization():
    """Test that the LLM can be initialized."""
    try:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=100  # Small value for testing
        )
        print("✅ LLM initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing LLM: {e}")
        return False

def run_tests():
    """Run all tests and report results."""
    env_test = test_environment_setup()
    llm_test = test_llm_initialization()
    
    print("\nTest results:")
    print(f"Environment setup: {'✅ PASSED' if env_test else '❌ FAILED'}")
    print(f"LLM initialization: {'✅ PASSED' if llm_test else '❌ FAILED'}")
    
    if env_test and llm_test:
        print("\n✅ All tests passed!")
        print("\nTo run the full agent, use: poetry run crypto-advisor")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests()) 