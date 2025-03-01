import pandas as pd
from typing import Type
from src.domain.strategy import TradingStrategy

class BacktestEngine:
    """
    A class for event-based backtesting of trading strategies.

    Attributes:
    ==========
    strategy: TradingStrategy
        The trading strategy to be tested.
    initial_cash: float
        The initial cash balance for backtesting.
    ftc: float
        Fixed transaction costs per trade (buy or sell).
    ptc: float
        Proportional transaction costs per trade (buy or sell).

    Methods:
    =======
    run_backtest:
        Executes the strategy over the dataset and calculates performance.
    """

    def __init__(self, strategy: Type[TradingStrategy], initial_cash=10_000, ftc=0.0, ptc=0.0):
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.ftc = ftc
        self.ptc = ptc
        self.position = 0  # Number of shares held
        self.trades = []
        self.results = None  # Stores the backtest results

    def execute_trade(self, date, price, action, units=None):
        """Executes a trade (buy/sell) and updates cash balance."""
        if units is None:
            units = int(self.cash / price)  # Invest full cash if no units specified

        cost = units * price * (1 + self.ptc) + self.ftc if action == "BUY" else units * price * (1 - self.ptc) - self.ftc

        if action == "BUY" and cost <= self.cash:
            self.cash -= cost
            self.position += units
            self.trades.append((date, price, "BUY", units))
        elif action == "SELL" and self.position >= units:
            self.cash += cost
            self.position -= units
            self.trades.append((date, price, "SELL", units))

    def run_backtest(self, data: pd.DataFrame):
        """Runs the backtest on historical data using the strategy."""
        # Compute indicators inside the strategy
        data = self.strategy.compute_indicators(data)

        for i, row in data.iterrows():
            date = row["timestamp"]
            price = row["close_price"]
            signal = self.strategy.generate_signal(row)

            if signal == "BUY":
                self.execute_trade(date, price, "BUY")
            elif signal == "SELL":
                self.execute_trade(date, price, "SELL")

        # Close out all positions
        if self.position > 0:
            self.execute_trade(date, price, "SELL", self.position)

        # Compute final portfolio value
        net_wealth = self.cash + (self.position * price)
        self.results = {
            "Final Balance": self.cash,
            "Final Net Wealth": net_wealth,
            "Performance (%)": ((net_wealth - self.initial_cash) / self.initial_cash) * 100,
            "Total Trades": len(self.trades),
        }
        return self.results
