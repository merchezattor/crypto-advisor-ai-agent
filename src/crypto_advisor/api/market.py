"""
Market data API.

This module handles requests for various market metrics and data.
"""

from crypto_advisor.api.models.market import (
    AltcoinDominanceRequest,
    HistoricalMarketDataRequest,
    FearGreedIndexRequest
)
from crypto_advisor.providers.coinmarketcap import (
    fetch_coinmarketcap_historical_data,
    fetch_altcoin_dominance,
    fetch_fear_greed_index
)

def get_historical_market_data_tool(request: HistoricalMarketDataRequest):
    """
    Fetches historical market data from CoinMarketCap.
    
    Args:
        request: A HistoricalMarketDataRequest object specifying time period
        
    Returns:
        Dictionary containing historical market data
    """
    return fetch_coinmarketcap_historical_data(request.days)

def get_altcoin_dominance_tool(request: AltcoinDominanceRequest):
    """
    Fetches Bitcoin vs. altcoin dominance data.
    
    Args:
        request: An AltcoinDominanceRequest object specifying time period
        
    Returns:
        Dictionary containing dominance data
    """
    return fetch_altcoin_dominance(request.days)

def get_fear_greed_index_tool(request: FearGreedIndexRequest):
    """
    Fetches Fear & Greed Index data.
    
    Args:
        request: A FearGreedIndexRequest object specifying time period
        
    Returns:
        Dictionary containing Fear & Greed Index data
    """
    return fetch_fear_greed_index(request.days) 