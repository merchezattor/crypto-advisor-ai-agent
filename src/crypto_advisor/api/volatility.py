"""
Volatility analysis API.

This module handles requests for volatility analysis of candlestick data.
"""

from crypto_advisor.api.models.technical import TechnicalAnalysisRequest
from crypto_advisor.services.ta_service import calculate_volatility_index

def analyze_volatility_tool(request: TechnicalAnalysisRequest):
    """
    Calculates a volatility index for the provided OHLCV data.
    
    Args:
        request: A TechnicalAnalysisRequest object containing candlestick data
        
    Returns:
        Dictionary containing volatility index results
    """
    return calculate_volatility_index(request.candlestick_data) 