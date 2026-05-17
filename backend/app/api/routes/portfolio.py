from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.schemas.portfolio_schema import (
    PortfolioCreate,
    PortfolioResponse,
    HoldingCreate,
)

from app.services.portfolio_service import (
    calculate_portfolio_summary
)

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/portfolio", response_model=PortfolioResponse)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db)
):
    new_portfolio = Portfolio(
        name=portfolio.name,
        owner_name=portfolio.owner_name
    )

    db.add(new_portfolio)

    db.commit()

    db.refresh(new_portfolio)

    return new_portfolio


@router.post("/portfolio/{portfolio_id}/holdings")
def add_holding(
    portfolio_id: int,
    holding: HoldingCreate,
    db: Session = Depends(get_db)
):
    new_holding = Holding(
        ticker=holding.ticker,
        quantity=holding.quantity,
        buy_price=holding.buy_price,
        portfolio_id=portfolio_id
    )

    db.add(new_holding)

    db.commit()

    db.refresh(new_holding)

    return new_holding


@router.get("/portfolio/{portfolio_id}",
            response_model=PortfolioResponse)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .first()
    )

    return portfolio

@router.get("/portfolio/{portfolio_id}/summary")
def get_portfolio_summary(
    portfolio_id: int,
    db: Session = Depends(get_db)
):

    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .first()
    )

    return calculate_portfolio_summary(portfolio,db)