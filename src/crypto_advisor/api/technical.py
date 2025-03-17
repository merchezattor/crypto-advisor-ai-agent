"""
Technical analysis API.

This module handles requests for technical analysis of candlestick data.
"""

from crypto_advisor.api.models.technical import TechnicalAnalysisRequest
from crypto_advisor.providers.binance import perform_technical_analysis

def analyze_technical_data_tool(request: TechnicalAnalysisRequest):
    """
    Performs technical analysis on the provided OHLCV data.
    
    Args:
        request: A TechnicalAnalysisRequest object containing candlestick data
        
    Returns:
        Dictionary containing technical analysis results
    """
    return perform_technical_analysis(request.candlestick_data) 