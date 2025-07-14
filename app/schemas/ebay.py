from pydantic import BaseModel
from datetime import datetime

class SearchResponse(BaseModel):
    keyword: str
    timestamp: datetime