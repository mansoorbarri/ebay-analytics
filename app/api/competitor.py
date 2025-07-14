from fastapi import APIRouter
from app.services.competitor_service import analyze_competitor
from app.schemas.competitor import CompetitorAnalysisResponse

router = APIRouter()

@router.get("/analyze", response_model=CompetitorAnalysisResponse)
async def competitor_analysis(seller_name: str):
    return await analyze_competitor(seller_name)