import httpx
from app.core.config import settings

EBAY_TOKEN_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

async def get_ebay_token():
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "client_credentials",
            "scope": settings.EBAY_SCOPE
        }
        auth = (settings.EBAY_CLIENT_ID, settings.EBAY_CLIENT_SECRET)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = await client.post(EBAY_TOKEN_URL, data=data, headers=headers, auth=auth)
        response.raise_for_status()
        return response.json()["access_token"]
