from src.infrastructure.config import get_settings

settings = get_settings()
# Define available data sources
DATA_SOURCES = {
    "yfinance": "src.infrastructure.data.yfinance",
    "alphavantage": "src.infrastructure.data.alphavantage",
    "binance": "src.infrastructure.data.binance_api",
}

