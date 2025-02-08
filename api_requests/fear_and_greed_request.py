from pydantic import BaseModel, Field

class FearGreedRequest(BaseModel):
    days: int = Field(30, description="Number of past days to retrieve the Fear & Greed Index for.")