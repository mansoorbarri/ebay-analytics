from fastapi import APIRouter
from app.services.sales_service import get_sales_chart
from app.schemas.sales import SalesChartResponse

router = APIRouter()

@router.get("/chart", response_model=SalesChartResponse)
async def sales_chart(product_id: str):
    return await get_sales_chart(product_id)