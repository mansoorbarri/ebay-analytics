from fastapi import FastAPI
from app.api import auth, ebay, competitor, sales, keywords, scraper
from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="eBaylytics API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(ebay.router, prefix="/ebay", tags=["eBay Search"])
app.include_router(competitor.router, prefix="/competitor", tags=["Competitor Analyzer"])
app.include_router(sales.router, prefix="/sales", tags=["Sales Charts"])
app.include_router(keywords.router, prefix="/keywords", tags=["Keyword Analytics"])
app.include_router(scraper.router, prefix="/scraper")
