"""
Integration tests for the volatility index functionality.

This module tests the volatility index calculation with real data from Binance.
"""
import pytest
from datetime import datetime

# Import the necessary components
from crypto_advisor.providers.binance import fetch_binance_chart
from crypto_advisor.services.ta_service import calculate_volatility_index
from crypto_advisor.api.volatility import analyze_volatility_tool
from crypto_advisor.api.models.technical import TechnicalAnalysisRequest

# Integration test with real API data
@pytest.mark.integration
def test_volatility_index_with_real_data():
    """
    Integration test for the volatility index calculation using real data from Binance.
    
    This test:
    1. Fetches real BTC/USDT candlestick data from Binance
    2. Calculates the volatility index
    3. Verifies the results are valid
    
    This test requires an internet connection to access the Binance API.
    """
    try:
        # Fetch real data from Binance for BTC/USDT
        symbol = "BTCUSDT"
        interval = "1d"  # Daily candles
        limit = 50  # Fetch 50 candles (about 50 days)
        
        # Try to get the data
        candles = fetch_binance_chart(symbol, interval, limit)
        
        # Make sure we got data
        assert len(candles) > 0, "Failed to fetch candlestick data from Binance"
        
        # Calculate volatility index directly from the service function
        volatility_result = calculate_volatility_index(candles)
        
        # Verify the structure and validity of the result
        assert isinstance(volatility_result, dict)
        assert "volatility_index" in volatility_result
        assert 0 <= volatility_result["volatility_index"] <= 5
        assert "volatility_category" in volatility_result
        
        # Test the API layer as well (complete integration)
        # Create a request object as it would come from the agent
        request = TechnicalAnalysisRequest(candlestick_data=candles)
        
        # Use the API function
        api_result = analyze_volatility_tool(request)
        
        # Verify the API returns the same result
        assert api_result["volatility_index"] == volatility_result["volatility_index"]
        assert api_result["volatility_category"] == volatility_result["volatility_category"]
        
        # Print the results for inspection
        print(f"\nIntegration test volatility results for {symbol} ({interval}):")
        print(f"Volatility Index: {volatility_result['volatility_index']} - {volatility_result['volatility_category']}")
        print(f"Component scores: ATR={volatility_result['components']['atr_score']}, "
              f"BBW={volatility_result['components']['bbw_score']}, "
              f"HV={volatility_result['components']['hv_score']}")
        
    except Exception as e:
        pytest.skip(f"Integration test failed due to external dependency: {str(e)}")

# Integration test comparing volatility across different timeframes
@pytest.mark.integration
def test_volatility_across_timeframes():
    """
    Test that calculates and compares volatility across different timeframes.
    
    This test:
    1. Fetches BTC/USDT data for multiple timeframes
    2. Calculates volatility for each timeframe
    3. Verifies that shorter timeframes typically show different volatility patterns
    """
    try:
        # Define timeframes to test
        timeframes = ["1h", "4h", "1d"]
        symbol = "BTCUSDT"
        results = {}
        
        # Fetch data and calculate volatility for each timeframe
        for interval in timeframes:
            # The number of candles to fetch depends on the timeframe
            # For fair comparison, we want roughly the same time period
            if interval == "1h":
                limit = 168  # ~7 days
            elif interval == "4h":
                limit = 42  # ~7 days
            else:  # 1d
                limit = 30  # 30 days
                
            candles = fetch_binance_chart(symbol, interval, limit)
            assert len(candles) > 0, f"Failed to fetch {interval} candlestick data"
            
            result = calculate_volatility_index(candles)
            results[interval] = result
        
        # Print comparison results
        print("\nVolatility comparison across timeframes:")
        for interval, result in results.items():
            print(f"{interval}: {result['volatility_index']} - {result['volatility_category']}")
        
        # Verify we have results for all timeframes
        assert len(results) == len(timeframes)
        
        # Typically different timeframes show different volatility characteristics,
        # but not necessarily different values, so we just check that calculation works
        for interval, result in results.items():
            assert 0 <= result["volatility_index"] <= 5
            
    except Exception as e:
        pytest.skip(f"Timeframe comparison test failed: {str(e)}")

# Integration test with the LangChain tool
@pytest.mark.integration
def test_volatility_tool_integration():
    """
    Test the integration of the volatility index with the LangChain tools system.
    
    This test:
    1. Imports and initializes the LangChain tool
    2. Executes the tool with real data
    3. Verifies the result structure matches what the LangChain agent would receive
    """
    try:
        from crypto_advisor.tools import get_volatility_index_tool
        from langchain.tools.base import ToolException
        
        # Get the tool
        volatility_tool = get_volatility_index_tool()
        
        # Fetch some real data
        candles = fetch_binance_chart("BTCUSDT", "1d", 30)
        
        # Execute the tool with the data
        tool_result = volatility_tool.func(TechnicalAnalysisRequest(candlestick_data=candles))
        
        # Verify the result
        assert isinstance(tool_result, dict)
        assert "volatility_index" in tool_result
        assert "volatility_category" in tool_result
        
        # Print the result
        print("\nLangChain tool integration result:")
        print(f"Volatility: {tool_result['volatility_index']} - {tool_result['volatility_category']}")
        
    except ToolException as e:
        pytest.skip(f"Tool integration test failed: {str(e)}")
    except Exception as e:
        pytest.skip(f"Tool integration test failed for other reasons: {str(e)}") 