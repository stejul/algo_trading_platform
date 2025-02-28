from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # General settings
    APP_ENV: str = "development"  # Options: development, testing, production
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Data source settings
    DEFAULT_DATA_SOURCE: str = "yfinance"  # Could be alphavantage, binance, etc. DEFINITION is in application:__init__.py
    YFINANCE_CACHE: bool = True  # Enable caching of Yahoo Finance data

    # API keys (set via environment variables)
    ALPHA_VANTAGE_API_KEY: str = ""
    BINANCE_API_KEY: str = ""

    # Database settings (for persistence)
    DB_URL: str = "sqlite:///data/trading.db"

    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_EXPIRATION_DAYS: int = 7
    CACHE_DIR: str = "cache/"

    # Logging
    LOG_FILE_PATH: str = "logs/trading_platform.log"

    class Config:
        env_file = ".env"  # Load variables from .env file
        env_file_encoding = "utf-8"

@lru_cache()  # Cache settings to avoid reloading
def get_settings() -> Settings:
    return Settings()
