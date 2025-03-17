"""
Technical analysis request models.

This module provides Pydantic models for technical analysis requests.
"""

from pydantic import BaseModel, Field
from typing import List, Dict

class TechnicalAnalysisRequest(BaseModel):
    """Model for technical analysis requests."""
    
    candlestick_data: List[Dict] = Field(
        ..., 
        description="List of OHLCV candlestick data."
    ) 