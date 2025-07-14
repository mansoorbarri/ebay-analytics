from pydantic import BaseModel
from typing import List

class SalesDataPoint(BaseModel):
    date: str
    units_sold: int
    revenue: float

class SalesChartResponse(BaseModel):
    product_name: str
    data: List[SalesDataPoint]