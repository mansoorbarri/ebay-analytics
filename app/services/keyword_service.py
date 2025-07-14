from app.services.ebay_auth import get_ebay_token
from app.core.config import settings
import httpx

async def keyword_analytics(seed_term: str):
    token = await get_ebay_token()
    url = f"{settings.EBAY_BASE}/buy/browse/v1/item_summary/search?q={seed_term}&limit=10"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        suggestions = []
        for item in data.get("itemSummaries", []):
            title = item.get("title", "").lower()
            if seed_term.lower() not in title:
                suggestions.append({
                    "keyword": title,
                    "volume": 100,  # Placeholder
                    "competition": "medium"  # Placeholder
                })

        return {
            "seed_term": seed_term,
            "suggestions": suggestions[:5]
        }
