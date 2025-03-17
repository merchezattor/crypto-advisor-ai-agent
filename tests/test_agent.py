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
    
    # Use an assertion instead of returning a value        
    assert all_keys_set, "Not all required environment variables are set"

def test_llm_initialization():
    """Test that the LLM can be initialized."""
    try:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=100  # Small value for testing
        )
        print("✅ LLM initialized successfully")
        # Use an assertion that is always true instead of returning True
        assert llm is not None, "LLM should be initialized"
    except Exception as e:
        print(f"❌ Error initializing LLM: {e}")
        assert False, f"LLM initialization failed: {str(e)}"

def run_tests():
    """Run all tests and report results."""
    # Create variables to track test results
    env_test_passed = True
    llm_test_passed = True
    
    try:
        test_environment_setup()
    except AssertionError as e:
        env_test_passed = False
    
    try:
        test_llm_initialization()
    except AssertionError as e:
        llm_test_passed = False
    
    print("\nTest results:")
    print(f"Environment setup: {'✅ PASSED' if env_test_passed else '❌ FAILED'}")
    print(f"LLM initialization: {'✅ PASSED' if llm_test_passed else '❌ FAILED'}")
    
    if env_test_passed and llm_test_passed:
        print("\n✅ All tests passed!")
        print("\nTo run the full agent, use: poetry run crypto-advisor")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests()) 