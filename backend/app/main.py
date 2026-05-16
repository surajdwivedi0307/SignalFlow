from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.stocks import router as stock_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
     "http://localhost:3000",
     "https://signal-flow-git-vercel-react-se-79f661-suraj-dwivedi-s-projects.vercel.app",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_router)


@app.get("/")
def home():
    return {"message": "Welcome to SignalFlow"}