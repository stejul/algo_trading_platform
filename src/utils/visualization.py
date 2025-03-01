import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from typing import Dict, Optional
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)

class TradingVisualizer:
    """
    A class for visualizing backtesting results, including market data, trading signals,
    portfolio performance, and strategy indicators.
    """

    @staticmethod
    def plot_candlestick_with_signals(
        market_data: pd.DataFrame,
        signals: Optional[pd.DataFrame] = None,
        title: str = "Candlestick Chart with Signals",
    ):
        """Plots a candlestick chart with optional buy/sell signals."""
        logger.info("Trying to plot candlestick with signals")
        try:
            if market_data.empty:
                logger.warning("Market data is empty, skipping candlestick plot.")
                return

            df = market_data.copy()
            df.index = pd.to_datetime(df["timestamp"])

            expected_cols = {
                "open_price": "Open",
                "high_price": "High",
                "low_price": "Low",
                "close_price": "Close",
                "volume": "Volume",
            }
            df = df.rename(columns=expected_cols)

            missing_cols = [col for col in ["Open", "High", "Low", "Close", "Volume"] if col not in df.columns]
            if missing_cols:
                logger.warning(f"Missing required columns {missing_cols}, skipping candlestick plot.")
                return

            fig, (ax_candle, ax_volume) = plt.subplots(
                2, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]}
            )
            mpf.plot(df, type="candle", ax=ax_candle, style="charles", volume=ax_volume)

            if signals is not None and "signal" in signals.columns:
                buy_signals = signals[signals["signal"] == "BUY"]
                sell_signals = signals[signals["signal"] == "SELL"]

                ax_candle.scatter(
                    buy_signals.index, buy_signals["Close"], 
                    marker="^", color="g", s=100, label="Buy Signal"
                )
                ax_candle.scatter(
                    sell_signals.index, sell_signals["Close"], 
                    marker="v", color="r", s=100, label="Sell Signal"
                )

            ax_candle.set_title(title)
            ax_candle.legend()
            plt.show()
        except Exception as e:
            logger.warning(f"Couldn't plot candlestick Chart: {e}")

    @staticmethod
    def plot_strategy_indicators(
        market_data: pd.DataFrame, strategy_name: str, title: str = "Market Data with Indicators"
    ):
        """
        Automatically detects and plots the relevant indicators for a given strategy.

        Args:
            market_data (pd.DataFrame): Market data containing price and indicators.
            strategy_name (str): The strategy for which to plot indicators.
            title (str): The title of the plot.
        """
        logger.info(f"Trying to plot indicators for {strategy_name}")

        try:
            df = market_data.copy()
            df.index = pd.to_datetime(df["timestamp"])

            strategy_indicators = {
                "SMAStrategy": ["short_sma", "long_sma"],
                "MomentumStrategy": ["momentum"],
                "MeanReversionStrategy": ["mean", "std", "zscore"],
            }

            if strategy_name not in strategy_indicators:
                logger.warning(f"Unknown strategy: {strategy_name}. No indicators available.")
                return

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df.index, df["close_price"], label="Close Price", color="blue")

            for col in strategy_indicators[strategy_name]:
                if col in df.columns:
                    ax.plot(df.index, df[col], label=col, linestyle="--")

            ax.set_title(title)
            ax.legend()
            plt.show()
        except Exception as e:
            logger.warning(f"Couldn't plot indicators for {strategy_name}: {e}")

    @staticmethod
    def plot_portfolio_value(portfolio_data: pd.DataFrame, title: str = "Portfolio Value Over Time"):
        """Plots portfolio value over time based on backtesting results."""
        try:
            df = portfolio_data.copy()
            df.index = pd.to_datetime(df["timestamp"])

            plt.figure(figsize=(12, 6))
            plt.plot(df.index, df["net_wealth"], label="Net Wealth", color="green")
            plt.xlabel("Date")
            plt.ylabel("Portfolio Value")
            plt.title(title)
            plt.legend()
            plt.grid()
            plt.show()
        except Exception as e:
            logger.warning(f"Couldn't plot portfolio value: {e}")

    @staticmethod
    def print_backtest_results(results: Dict[str, float]):
        """Prints the final results of the backtest."""
        print("=" * 50)
        print(" Backtest Performance Summary ")
        print("=" * 50)
        for key, value in results.items():
            print(f"{key}: {value:.2f}")
        print("=" * 50)
