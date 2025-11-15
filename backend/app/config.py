import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/postgres")
    API_KEY: str = os.getenv("API_KEY", "changemeapikey")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "ProsusAI/finbert")
    TICKER_WATCHLIST: str = os.getenv("TICKER_WATCHLIST", "AAPL,TSLA,MSFT,GOOG,AMZN,NVDA,JPM,BAC,BRK.A,SPY")

settings = Settings()