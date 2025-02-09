from pydantic import BaseModel, Field
from typing import List, Dict

class PatternRecognitionRequest(BaseModel):
    candlestick_data: List[Dict] = Field(..., description="List of OHLCV candlestick data.")
