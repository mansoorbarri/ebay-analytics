from pydantic import BaseModel
from typing import List

class KeywordSuggestion(BaseModel):
    keyword: str
    volume: int
    competition: str

class KeywordAnalyticsResponse(BaseModel):
    seed_term: str
    suggestions: List[KeywordSuggestion]