from fastapi import APIRouter, Query
from app.services.scraper_service import get_sold_count, get_top_items_sold_by_keyword

router = APIRouter()

@router.get("/sold-count")
async def sold_count_api(item_url: str = Query(..., description="Full eBay item URL")):
    return get_sold_count(item_url)

@router.get("/keyword-sales")
async def keyword_sales_api(keyword: str = Query(..., description="eBay product keyword")):
    return get_top_items_sold_by_keyword(keyword)
