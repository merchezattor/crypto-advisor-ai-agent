from pydantic import BaseModel, Field

class AltcoinDominanceRequest(BaseModel):
    days: int = Field(30, description="Number of past days to retrieve Bitcoin and altcoin dominance data for.")