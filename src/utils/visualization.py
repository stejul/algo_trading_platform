import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import mplfinance as mpf
from typing import Dict, List, Optional, Tuple, Union

from src.infrastructure.logging import get_logger

logger = get_logger(__name__)

class TradingVisualizer:
    """Class for visualizing market data and trading signals dynamically."""
    @staticmethod
    def plot_candlestick_with_signals(
        market_data: pd.DataFrame,
        signals: Optional[pd.DataFrame] = None,
        title: str = "Candlestick Chart with Signals",
    ):
        """Plots a candlestick chart with optional buy/sell signals."""

        df = market_data.copy()
        df.index = pd.to_datetime(df["timestamp"])

        df = df.rename(
            columns={
                "open_price": "Open",
                "high_price": "High",
                "low_price": "Low",
                "close_price": "Close",
                "volume": "Volume",
            }
        )

        fig, (ax_candle, ax_volume) = plt.subplots(2, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]})

        mpf.plot(df, type="candle", volume=ax_volume, ax=ax_candle, style="charles")

        # Add Buy/Sell signals
        if signals is not None:
            buy_signals = signals[signals["signal"] == 1]
            sell_signals = signals[signals["signal"] == -1]

            ax_candle.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="g", s=100, label="Buy Signal")
            ax_candle.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="r", s=100, label="Sell Signal")

        ax_candle.set_title(title)
        ax_candle.legend()
        plt.show()

    @staticmethod
    def plot_indicators(
        market_data: pd.DataFrame,
        indicators: Dict[str, str],
        title: str = "Market Data with Indicators",
        signals: Optional[pd.DataFrame] = None,
    ):
        """
        Generic function to plot indicators (e.g., SMA, Bollinger Bands, Momentum).

        Args:
            market_data (pd.DataFrame): The market data with close prices.
            indicators (Dict[str, str]): Dictionary of indicator names and their corresponding columns in the DataFrame.
            title (str): Chart title.
            signals (Optional[pd.DataFrame]): Buy/Sell signals DataFrame.
        """
        df = market_data.copy()
        df.index = pd.to_datetime(df["timestamp"])

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df.index, df["close_price"], label="Close Price", color="blue")

        for label, column in indicators.items():
            if column in df.columns:
                ax.plot(df.index, df[column], label=label, linestyle="--")

        if signals is not None:
            buy_signals = signals[signals["signal"] == 1]
            sell_signals = signals[signals["signal"] == -1]

            ax.scatter(buy_signals.index, buy_signals["close_price"], marker="^", color="g", s=100, label="Buy Signal")
            ax.scatter(sell_signals.index, sell_signals["close_price"], marker="v", color="r", s=100, label="Sell Signal")

        ax.set_title(title)
        ax.legend()
        plt.show()
