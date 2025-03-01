import pandas as pd
from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    """ Abstract Base Class for Trading Strategies. """

    @abstractmethod
    def compute_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Computes the required indicators and returns the modified dataframe. """
        pass

    @abstractmethod
    def generate_signal(self, row: pd.Series):
        """ Given a row of market data, generate a trading signal. """
        pass


class SMAStrategy(TradingStrategy):
    """ Simple Moving Average (SMA) Crossover Strategy. """

    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def compute_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Computes the short and long SMAs. """
        data["short_sma"] = data["close_price"].rolling(window=self.short_window).mean()
        data["long_sma"] = data["close_price"].rolling(window=self.long_window).mean()
        return data

    def generate_signal(self, row: pd.Series):
        """ Generates a BUY/SELL signal based on SMA crossover. """
        if row["short_sma"] > row["long_sma"]:
            return "BUY"
        elif row["short_sma"] < row["long_sma"]:
            return "SELL"
        return "HOLD"


class MomentumStrategy(TradingStrategy):
    """ Momentum-Based Strategy. """

    def __init__(self, lookback=14):
        self.lookback = lookback

    def compute_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Computes momentum based on past returns. """
        data["momentum"] = data["close_price"].pct_change(self.lookback)
        return data

    def generate_signal(self, row: pd.Series):
        """ Generates a BUY/SELL signal based on momentum. """
        if row["momentum"] > 0:
            return "BUY"
        elif row["momentum"] < 0:
            return "SELL"
        return "HOLD"


class MeanReversionStrategy(TradingStrategy):
    """ Mean Reversion Strategy. """

    def __init__(self, window=50, threshold=2):
        self.window = window
        self.threshold = threshold

    def compute_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Computes Z-score for mean reversion. """
        data["mean"] = data["close_price"].rolling(window=self.window).mean()
        data["std"] = data["close_price"].rolling(window=self.window).std()
        data["zscore"] = (data["close_price"] - data["mean"]) / data["std"]
        return data

    def generate_signal(self, row: pd.Series):
        """ Generates a BUY/SELL signal based on mean reversion. """
        if row["zscore"] < -self.threshold:
            return "BUY"
        elif row["zscore"] > self.threshold:
            return "SELL"
        return "HOLD"

class RSIStrategy(TradingStrategy):
    """ Relative Strength Index (RSI) Trading Strategy. """

    def __init__(self, period=14, overbought=70, oversold=30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    def compute_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Computes the RSI indicator. """
        delta = data["close_price"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        data["RSI"] = 100 - (100 / (1 + rs))
        return data

    def generate_signal(self, row: pd.Series):
        """ Generates trade signals based on RSI levels. """
        if row["RSI"] < self.oversold:
            return "BUY"
        elif row["RSI"] > self.overbought:
            return "SELL"
        return None
