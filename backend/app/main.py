from fastapi import FastAPI

from app.api.routes.stocks import router as stock_router

app = FastAPI()

app.include_router(stock_router)


@app.get("/")
def home():
    return {"message": "Welcome to SignalFlow"}