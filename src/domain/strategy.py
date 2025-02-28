import pandas as pd
from abc import ABC, abstractmethod
from src.infrastructure.logging import get_logger
from src.infrastructure.config import get_settings

logger = get_logger(__name__)
settings = get_settings()

class TradingStrategy(ABC):
    """Abstract Base Class for Trading Strategies"""

    @abstractmethod
    def generate_signals(self, market_data: pd.DataFrame) -> pd.DataFrame:
        """Generate buy/sell signals based on market data. Must be implemented by subclasses."""
        pass

class SMAStrategy(TradingStrategy):
    """Simple Moving Average (SMA) Crossover Strategy."""
    def __init__(self, short_window: int = 50, long_window: int = 200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, market_data: pd.DataFrame) -> pd.DataFrame:
        df = market_data.copy()
        df["SMA_Short"] = df["close_price"].rolling(window=self.short_window, min_periods=1).mean()
        df["SMA_Long"] = df["close_price"].rolling(window=self.long_window, min_periods=1).mean()

        df["signal"] = 0
        df.loc[df["SMA_Short"] > df["SMA_Long"], "signal"] = 1  # Buy Signal
        df.loc[df["SMA_Short"] < df["SMA_Long"], "signal"] = -1  # Sell Signal
        
        return df

class MomentumStrategy(TradingStrategy):
    """Momentum Trading Strategy."""
    def __init__(self, lookback_period: int = 14):
        self.lookback_period = lookback_period

    def generate_signals(self, market_data: pd.DataFrame) -> pd.DataFrame:
        df = market_data.copy()
        df["momentum"] = df["close_price"].diff(self.lookback_period)

        df["signal"] = 0
        df.loc[df["momentum"] > 0, "signal"] = 1  # Uptrend → Buy
        df.loc[df["momentum"] < 0, "signal"] = -1  # Downtrend → Sell
        
        return df

class MeanReversionStrategy(TradingStrategy):
    """Mean Reversion Trading Strategy using Bollinger Bands."""
    def __init__(self, window: int = 20, num_std_dev: float = 2):
        self.window = window
        self.num_std_dev = num_std_dev

    def generate_signals(self, market_data: pd.DataFrame) -> pd.DataFrame:
        df = market_data.copy()
        df["rolling_mean"] = df["close_price"].rolling(window=self.window, min_periods=1).mean()
        df["rolling_std"] = df["close_price"].rolling(window=self.window, min_periods=1).std()

        df["upper_band"] = df["rolling_mean"] + (self.num_std_dev * df["rolling_std"])
        df["lower_band"] = df["rolling_mean"] - (self.num_std_dev * df["rolling_std"])

        df["signal"] = 0
        df.loc[df["close_price"] < df["lower_band"], "signal"] = 1  # Buy
        df.loc[df["close_price"] > df["upper_band"], "signal"] = -1  # Sell
        
        return df
