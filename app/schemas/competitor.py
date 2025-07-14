from pydantic import BaseModel
from typing import List

class CompetitorItem(BaseModel):
    title: str
    price: float
    sold: int

class CompetitorAnalysisResponse(BaseModel):
    seller_name: str
    total_items: int
    total_sales: int
    top_products: List[CompetitorItem]