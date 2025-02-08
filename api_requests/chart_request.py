from pydantic import BaseModel, Field
from crypto import fetch_binance_chart

class ChartRequest(BaseModel):
    symbol: str = Field(description="The cryptocurrency trading pair, e.g., BTCUSDT, ETHUSDT.")
    interval: str = Field(description="Timeframe for the chart, e.g., 1m, 5m, 1h, 4h, 1d, 1w.")
    limit: int = Field(alias="num_candles", description="Number of candles to fetch, e.g., 10, 50, 100.")

    class Config:
        # Allow the model to accept input data using the alias "num_candles"
        allow_population_by_alias = True
        # Also allow population by the field name if needed
        allow_population_by_field_name = True
 
def fetch_chart_data_tool(request: ChartRequest):
    """Fetches candlestick chart data from Binance based on user request."""
    return fetch_binance_chart(request.symbol, request.interval, request.limit)