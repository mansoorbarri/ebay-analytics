from app.services.ebay_auth import get_ebay_token
import httpx
from app.core.config import settings  # Make sure this import points to your settings module

async def search_ebay_items(keyword: str):
    token = await get_ebay_token()

    url = f"{settings.EBAY_BASE}/buy/browse/v1/item_summary/search?q={keyword}&limit=5"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return {
            "keyword": keyword,
            "results": [
                {
                    "title": item.get("title"),
                    "price": item.get("price", {}).get("value"),
                    "currency": item.get("price", {}).get("currency"),
                    "condition": item.get("condition"),
                    "seller": item.get("seller", {}).get("username"),
                    "item_id": item.get("itemId")
                } for item in data.get("itemSummaries", [])
            ]
        }
