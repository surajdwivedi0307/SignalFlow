from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.portfolio import router as portfolio_router

from app.api.routes.stocks import router as stock_router

from app.models.stock import Stock
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.models.portfolio_snapshot import PortfolioSnapshot

from app.core.database import Base, engine



app = FastAPI()


Base.metadata.create_all(bind=engine)
print("DATABASE TABLES CREATED")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
     "http://localhost:3000",
     "https://signal-flow.vercel.app",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_router)
app.include_router(portfolio_router)

@app.get("/")
def home():
    return {"message": "Welcome to SignalFlow"}