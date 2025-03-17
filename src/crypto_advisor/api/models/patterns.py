"""
Pattern recognition request models.

This module provides Pydantic models for pattern recognition requests.
"""

from pydantic import BaseModel, Field
from typing import List, Dict

class PatternRecognitionRequest(BaseModel):
    """Model for pattern recognition requests."""
    
    candlestick_data: List[Dict] = Field(
        ..., 
        description="List of OHLCV candlestick data."
    ) 