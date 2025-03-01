import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from typing import Dict, Optional, Union
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)

class TradingVisualizer:
    """
    A class for visualizing backtesting results, including market data, trading signals,
    portfolio performance, risk metrics, and strategy indicators.
    """

    @staticmethod
    def plot_candlestick_with_signals(market_data: pd.DataFrame, signals: Optional[pd.DataFrame] = None, title: str = "Candlestick Chart with Signals"):
        """Plots a candlestick chart with optional buy/sell signals."""
        logger.info("Trying to plot candlestick with signals")
        try:
            if market_data.empty:
                logger.warning("Market data is empty, skipping candlestick plot.")
                return

            df = market_data.copy()
            df.index = pd.to_datetime(df["timestamp"])

            expected_cols = {"open_price": "Open", "high_price": "High", "low_price": "Low", "close_price": "Close", "volume": "Volume"}
            df = df.rename(columns=expected_cols)

            missing_cols = [col for col in ["Open", "High", "Low", "Close", "Volume"] if col not in df.columns]
            if missing_cols:
                logger.warning(f"Missing required columns {missing_cols}, skipping candlestick plot.")
                return

            fig, ax = plt.subplots(figsize=(12, 6))
            mpf.plot(df, type='candle', ax=ax, style='charles', volume=False)
            ax.set_title(title)  
            plt.show()
        except Exception as e:
            logger.warning(f"Couldn't plot candlestick chart: {e}")

    @staticmethod
    def plot_position_sizing(trades: pd.DataFrame):
        """Plots position sizing over time."""
        if trades.empty or "timestamp" not in trades or "Position Size" not in trades:
            logger.warning("Skipping position sizing plot: Required data missing.")
            return

        trades = trades.copy()
        trades["timestamp"] = pd.to_datetime(trades["timestamp"])
        trades.set_index("timestamp", inplace=True)

        plt.figure(figsize=(12, 6))
        plt.bar(trades.index, trades["Position Size"], color="purple", alpha=0.6)
        plt.title("Position Size Over Time")
        plt.xlabel("Date")
        plt.ylabel("Position Size")
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()
        logger.info("Position sizing plot generated successfully")

    @staticmethod
    def plot_stop_loss_levels(data: pd.DataFrame, stop_loss_prices: pd.Series):
        """Plots stop-loss levels alongside stock prices."""
        if not isinstance(stop_loss_prices, pd.Series):
            logger.error("Expected a Pandas Series for stop-loss prices but received a different type.")
            return

        if stop_loss_prices.empty:
            logger.warning("Skipping stop-loss plot: 'Stop Loss Price' data is missing.")
            return

        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['close_price'], label='Close Price', color='blue', alpha=0.6)
        plt.plot(data.index, stop_loss_prices, label='Stop Loss Level', linestyle='--', color='red')
        plt.legend()
        plt.title("Stop Loss Levels vs Price")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid()
        plt.show()
        logger.info("Stop-loss level plot generated successfully")


    @staticmethod
    def plot_portfolio_value(portfolio_data: pd.DataFrame, title: str = "Portfolio Value Over Time"):
        """Plots portfolio value over time based on backtesting results."""
        try:
            if portfolio_data.empty or "timestamp" not in portfolio_data or "net_wealth" not in portfolio_data:
                logger.warning("Skipping portfolio value plot: Required data missing.")
                return

            portfolio_data = portfolio_data.copy()
            portfolio_data["timestamp"] = pd.to_datetime(portfolio_data["timestamp"])
            portfolio_data.set_index("timestamp", inplace=True)

            plt.figure(figsize=(12, 6))
            plt.plot(portfolio_data.index, portfolio_data["net_wealth"], label="Net Wealth", color="green")
            plt.xlabel("Date")
            plt.ylabel("Portfolio Value")
            plt.title(title)
            plt.legend()
            plt.grid()
            plt.show()
            logger.info("Portfolio value plot generated successfully")
        except Exception as e:
            logger.warning(f"Couldn't plot portfolio value: {e}")


    @staticmethod
    def plot_drawdown(portfolio_values: pd.Series, max_drawdown: float):
        """ Plots the portfolio value with drawdown levels. """
        if portfolio_values is None or portfolio_values.empty:
            logger.warning("Skipping drawdown plot: Portfolio values are empty.")
            return

        portfolio_values = portfolio_values.copy()
        portfolio_values.index = pd.to_datetime(portfolio_values.index)

        drawdown = portfolio_values / portfolio_values.cummax() - 1

        plt.figure(figsize=(12, 6))
        plt.plot(portfolio_values, label="Portfolio Value", color="black")
        plt.fill_between(portfolio_values.index, portfolio_values, portfolio_values.cummax() * (1 - max_drawdown),
                         color="red", alpha=0.3, label="Max Drawdown Zone")
        plt.legend()
        plt.title("Portfolio Value and Drawdown")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.grid()
        plt.show()
        logger.info("Drawdown plot generated successfully")

    @staticmethod
    def print_backtest_results(results: Dict[str, Union[float, pd.Series]]):
        """Prints the final results of the backtest."""
        print("=" * 50)
        print(" Backtest Performance Summary ")
        print("=" * 50)
        for key, value in results.items():
            if isinstance(value, pd.Series):
                print(f"{key}: Series with {len(value)} values")
            else:
                print(f"{key}: {value:.2f}")
        print("=" * 50)
        logger.info("Backtest results printed successfully")
