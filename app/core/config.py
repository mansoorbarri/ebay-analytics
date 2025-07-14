import os
from dotenv import load_dotenv

load_dotenv()

# class Settings:
#     SECRET_KEY = os.getenv("SECRET_KEY", "secret")
#     ALGORITHM = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES = 60
#     EBAY_APP_ID = os.getenv("EBAY_APP_ID", "")

# settings = Settings()


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID", "")
    EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET", "")
    EBAY_SCOPE = os.getenv("EBAY_SCOPE", "https://api.ebay.com/oauth/api_scope")
    EBAY_BASE = os.getenv("EBAY_BASE", "https://api.sandbox.ebay.com")
settings = Settings()