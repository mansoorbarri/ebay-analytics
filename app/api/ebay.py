from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.search import SearchHistory
from app.api.auth import get_current_user
from app.services.ebay_service import search_ebay_items

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search")
async def search(keyword: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = await search_ebay_items(keyword)
    db_record = SearchHistory(user_id=current_user.id, keyword=keyword)
    db.add(db_record)
    db.commit()
    return result