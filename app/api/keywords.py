from fastapi import APIRouter
from app.services.keyword_service import keyword_analytics
from app.schemas.keyword import KeywordAnalyticsResponse

router = APIRouter()

@router.get("/analytics", response_model=KeywordAnalyticsResponse)
async def keyword_analytics_api(seed_term: str):
    return await keyword_analytics(seed_term)