"""
Market data request models.

This module provides Pydantic models for market data requests.
"""

from pydantic import BaseModel, Field

class AltcoinDominanceRequest(BaseModel):
    """Model for altcoin dominance requests."""
    
    days: int = Field(
        30, 
        description="Number of past days to retrieve Bitcoin and altcoin dominance data for."
    )

class HistoricalMarketDataRequest(BaseModel):
    """Model for historical market data requests."""
    
    days: int = Field(
        30, 
        description="Number of past days to retrieve market data for."
    )

class FearGreedIndexRequest(BaseModel):
    """Model for Fear & Greed index requests."""
    
    days: int = Field(
        30, 
        description="Number of past days to retrieve Fear & Greed Index data for."
    ) 