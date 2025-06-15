"""
Tests for the volatility index functionality.
"""
import pytest
import json
import pandas as pd
from datetime import datetime, timedelta

from crypto_advisor.services.ta_service import calculate_volatility_index

@pytest.fixture
def sample_candlestick_data():
    """Generate sample candlestick data for testing."""
    data = []
    base_time = datetime.now()
    close_price = 1000.0
    
    # Create sample data with some volatility
    for i in range(50):
        # Add some volatility every 10 candles
        if i % 10 == 0:
            volatility_factor = 2.0
        else:
            volatility_factor = 1.0
            
        time = base_time - timedelta(hours=i * 4)
        open_price = close_price
        high_price = open_price * (1 + 0.02 * volatility_factor)
        low_price = open_price * (1 - 0.015 * volatility_factor)
        close_price = open_price * (1 + 0.005 * (i % 5 - 2) * volatility_factor)
        volume = 1000 * (1 + 0.1 * volatility_factor)
        
        data.append({
            "time": time.isoformat(),
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        })
    
    # Return reversed data to have chronological order
    return list(reversed(data))

def test_calculate_volatility_index(sample_candlestick_data):
    """Test the volatility index calculation function."""
    # Call the function with sample data
    result = calculate_volatility_index(sample_candlestick_data)
    
    # Basic validation of the result structure
    assert isinstance(result, dict)
    assert "volatility_index" in result
    assert "volatility_category" in result
    assert "components" in result
    assert "raw_values" in result
    
    # Validate numeric values
    assert 0 <= result["volatility_index"] <= 5
    assert all(0 <= result["components"][key] <= 5 for key in ["atr_score", "bbw_score", "hv_score"])
    
    # Validate category
    assert result["volatility_category"] in ["Very Low", "Low", "Moderate", "High", "Very High"]

    # Ensure category matches the volatility_index value
    if result["volatility_index"] < 1:
        expected_category = "Very Low"
    elif result["volatility_index"] < 2:
        expected_category = "Low"
    elif result["volatility_index"] < 3:
        expected_category = "Moderate"
    elif result["volatility_index"] < 4:
        expected_category = "High"
    else:
        expected_category = "Very High"
    assert result["volatility_category"] == expected_category
    
    # Validate that raw values are present
    assert all(key in result["raw_values"] for key in ["atr", "bbw", "hv"])
    
    print(f"Volatility test result: {json.dumps(result, indent=2)}") 