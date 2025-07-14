from app.services.ebay_auth import get_ebay_token
from app.core.config import settings
import httpx
from datetime import datetime, timedelta
import random

async def get_sales_chart(item_id: str):
    token = await get_ebay_token()
    url = f"{settings.EBAY_BASE}/buy/browse/v1/item/{item_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        item = response.json()

    product_name = item.get("title", "Unknown Product")
    price = float(item.get("price", {}).get("value", 0.0))

    # Simulate sales over last 7 days
    today = datetime.now()
    data = []
    for i in range(7):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        units_sold = random.randint(5, 25)
        revenue = round(units_sold * price, 2)
        data.append({
            "date": date,
            "units_sold": units_sold,
            "revenue": revenue
        })

    return {
        "product_name": product_name,
        "data": data[::-1]  # oldest to newest
    }
