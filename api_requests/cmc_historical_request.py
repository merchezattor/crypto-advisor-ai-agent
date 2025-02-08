from pydantic import BaseModel, Field

class CMCHistoricalRequest(BaseModel):
    days: int = Field(30, description="Number of past days to retrieve historical global market data for.")