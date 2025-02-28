from src.infrastructure.data.yfinance import fetch_historical_data
from src.domain.models import MarketData
from src.infrastructure.logging import get_logger
from src.infrastructure.config import get_settings
import pandas as pd
import os
import pickle
import hashlib
import datetime as dt
from typing import List

settings = get_settings()
logger = get_logger(__name__)

class MarketDataService:
    """
    Service class to fetch and process market data.
    """

    def __init__(self, data_source=settings.DEFAULT_DATA_SOURCE):
        self.data_source = data_source
        self.cache_dir = settings.CACHE_DIR
        self.cache_enabled = settings.CACHE_ENABLED
        self.cache_expiration_days = settings.CACHE_EXPIRATION_DAYS
        
        if self.cache_enabled:
            os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_filepath(self, symbol, start_date, end_date):
        """Generates a unique cache file path based on the request parameters."""
        hash_key = hashlib.md5(f"{symbol}_{start_date}_{end_date}".encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.pkl")

    def _is_cache_valid(self, filepath):
        """Checks if the cache file is still valid based on expiration settings."""
        if not os.path.exists(filepath):
            return False
        
        file_modified_time = dt.datetime.fromtimestamp(os.path.getmtime(filepath))
        expiration_time = file_modified_time + dt.timedelta(days=self.cache_expiration_days)
        
        return dt.datetime.now() < expiration_time
    

    def get_historical_data(self, symbol, start_date, end_date):
        """Fetches market data with optional caching."""
        cache_file = self._get_cache_filepath(symbol, start_date, end_date)

        if self.cache_enabled and self._is_cache_valid(cache_file):
            logger.info(f"Loading cached data for {symbol} from {cache_file}")
            with open(cache_file, "rb") as f:
                return pickle.load(f)

        # Fetch data from the selected source
        logger.info(f"Fetching fresh data for {symbol} from {self.data_source}...")
        data = fetch_historical_data(symbol, start_date, end_date)

        # Convert to Pandas DataFrame
        data_dict = [entry.model_dump() for entry in data]

        df = pd.DataFrame(data_dict, columns=["symbol", "timestamp", "open_price", "high_price", "low_price", "close_price", "volume"])

        # Store in cache if enabled
        if self.cache_enabled:
            with open(cache_file, "wb") as f:
                pickle.dump(df, f)
            logger.info(f"Cached data saved at {cache_file}")

        return df
