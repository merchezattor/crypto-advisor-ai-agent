from pydantic import BaseModel, Field
from typing import List, Dict

class TechnicalAnalysisRequest(BaseModel):
    candlestick_data: List[Dict] = Field(..., description="List of OHLCV candlestick data.")