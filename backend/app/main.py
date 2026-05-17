from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.portfolio import router as portfolio_router

from app.api.routes.stocks import router as stock_router

from app.models.stock import Stock
from app.models.portfolio import Portfolio
from app.models.holding import Holding

app = FastAPI()
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