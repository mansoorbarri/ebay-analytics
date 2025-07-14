from app.services.ebay_auth import get_ebay_token
import httpx

async def analyze_competitor(seller_name: str):
    token = await get_ebay_token()
    from app.core.config import settings

    url = f"{settings.EBAY_BASE}/buy/browse/v1/item_summary/search?seller={seller_name}&limit=5"

    # url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?seller={seller_name}&limit=5"

    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        top_products = []
        for item in data.get("itemSummaries", []):
            price = item.get("price", {}).get("value")
            title = item.get("title")
            # NOTE: Sold count not available — mock or use another strategy
            top_products.append({"title": title, "price": float(price), "sold": 0})

        return {
            "seller_name": seller_name,
            "total_items": len(top_products),
            "total_sales": 0,  # Replace if you can infer sales
            "top_products": top_products
        }
