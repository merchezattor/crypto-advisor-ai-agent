"""
Chart data request API.

This module handles requests for chart data from cryptocurrency exchanges.
"""

from crypto_advisor.api.models.chart import ChartRequest
from crypto_advisor.providers.binance import fetch_binance_chart

def fetch_chart_data_tool(request: ChartRequest):
    """
    Fetches candlestick chart data from Binance based on user request.
    
    Args:
        request: A ChartRequest object containing the symbol, interval, and number of candles
        
    Returns:
        A pandas DataFrame containing the chart data
    """
    return fetch_binance_chart(request.symbol, request.interval, request.limit) 