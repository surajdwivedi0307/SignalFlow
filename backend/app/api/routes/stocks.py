from fastapi import APIRouter

from app.services.stock_service import (
    get_stock_data,
    get_stock_history
)

from app.schemas.stock_schema import (
    StockResponse,
    HistoryResponse
)



router = APIRouter()


@router.get("/stocks/{ticker}", response_model=StockResponse)
def get_stock(ticker: str):
    return get_stock_data(ticker)

@router.get(
    "/stocks/{ticker}/history",
    response_model=HistoryResponse
)
def stock_history(ticker: str, period: str = "1mo"):
    return get_stock_history(ticker, period)