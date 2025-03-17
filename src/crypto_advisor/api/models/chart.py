"""
Chart data request models.

This module provides Pydantic models for chart data requests.
"""

from pydantic import BaseModel, Field

class ChartRequest(BaseModel):
    """Model for chart data requests."""
    
    symbol: str = Field(description="The cryptocurrency trading pair, e.g., BTCUSDT, ETHUSDT.")
    interval: str = Field(description="Timeframe for the chart, e.g., 1m, 5m, 1h, 4h, 1d, 1w.")
    limit: int = Field(alias="num_candles", description="Number of candles to fetch, e.g., 10, 50, 100.")

    class Config:
        """Configuration for the ChartRequest model."""
        # Allow the model to accept input data using the alias "num_candles"
        allow_population_by_alias = True
        # Also allow population by the field name if needed
        allow_population_by_field_name = True 