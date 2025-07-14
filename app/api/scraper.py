# app/api/scraper.py

from fastapi import APIRouter, Query
from app.services.scraper_service import get_sold_count, get_top_items_sold_by_keyword, init_driver # Import init_driver here!

router = APIRouter()

@router.get("/sold-count")
async def sold_count_api(item_url: str = Query(..., description="Full eBay item URL")):
    driver = None # Initialize driver variable to None
    try:
        driver = init_driver() # Initialize the Selenium WebDriver
        # Pass the driver instance as the first argument
        return get_sold_count(driver, item_url)
    finally:
        if driver: # Ensure driver exists before trying to quit it
            driver.quit()

@router.get("/keyword-sales")
async def keyword_sales_api(keyword: str = Query(..., description="eBay product keyword")):
    # get_top_items_sold_by_keyword already handles its own driver initialization internally
    # for the search page, and then creates separate drivers for concurrent item pages.
    return get_top_items_sold_by_keyword(keyword)