from pydantic import BaseModel
from typing import List, Optional


class HoldingCreate(BaseModel):
    ticker: str
    quantity: float
    buy_price: float


class HoldingResponse(BaseModel):
    id: int
    ticker: str
    quantity: float
    buy_price: float

    class Config:
        from_attributes = True


class PortfolioCreate(BaseModel):
    name: str
    owner_name: Optional[str] = None


class PortfolioResponse(BaseModel):
    id: int
    name: str
    owner_name: Optional[str]
    holdings: List[HoldingResponse] = []

    class Config:
        from_attributes = True