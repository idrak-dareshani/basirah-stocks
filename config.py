from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FMP_API_KEY: str | None = None
    DATA_PROVIDER: str = "yfinance"
    class Config:
        env_file = ".env"

settings = Settings()
