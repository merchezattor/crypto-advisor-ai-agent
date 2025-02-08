from pydantic import BaseModel, Field
from crypto import analyze_binance_data

class AnalysisRequest(BaseModel):
    symbol: str = Field(..., description="The cryptocurrency trading pair, e.g., BTCUSDT.")
    interval: str = Field(..., description="Timeframe for chart data, e.g., 1h, 4h.")
    limit: int = Field(..., alias="num_candles", description="Number of candles to analyze.")
    
    class Config:
        allow_population_by_alias = True
        allow_population_by_field_name = True

def analyze_chart_data(request: AnalysisRequest):
    """Analyze candlestick chart data from Binance for technical analysis."""
    return analyze_binance_data(request.symbol, request.interval, request.limit)