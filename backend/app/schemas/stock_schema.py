from pydantic import BaseModel
from typing import Optional


class StockResponse(BaseModel):
    ticker: str
    company_name: Optional[str]
    current_price: Optional[float]
    market_cap: Optional[int]
    sector: Optional[str]
    industry: Optional[str]

class HistoryPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class HistoryResponse(BaseModel):
    ticker: str
    period: str
    history: list[HistoryPoint]