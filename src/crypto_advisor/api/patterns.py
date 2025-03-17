"""
Pattern recognition API.

This module handles requests for pattern recognition from candlestick data.
"""

from crypto_advisor.api.models.patterns import PatternRecognitionRequest
from crypto_advisor.providers.binance import detect_selected_patterns

def recognize_patterns_tool(request: PatternRecognitionRequest):
    """
    Detects candlestick patterns in the provided OHLCV data.
    
    Args:
        request: A PatternRecognitionRequest object containing candlestick data
        
    Returns:
        Dictionary containing detected patterns
    """
    return detect_selected_patterns(request.candlestick_data) 