import pandas as pd
from typing import Type, Dict, Tuple
from itertools import product
import numpy as np
from src.domain.strategy import TradingStrategy
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)

class BacktestEngine:
    """
    A class for event-based backtesting of trading strategies.
    """

    def __init__(self, strategy: Type[TradingStrategy], initial_cash=10_000, ftc=0.0, ptc=0.0):
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.ftc = ftc
        self.ptc = ptc
        self.position = 0  # Number of shares held
        self.trades = []
        self.results = {}  # Stores the backtest results

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
        data["Position Size"] = 0  # Initialize position size
        portfolio_values = []

        for i, row in data.iterrows():
            date = row["timestamp"]
            price = row["close_price"]
            signal = self.strategy.generate_signal(row)

            if signal == "BUY":
                self.execute_trade(date, price, "BUY")
            elif signal == "SELL":
                self.execute_trade(date, price, "SELL")

            data.at[i, "Position Size"] = self.position
            portfolio_values.append(self.cash + (self.position * price))

        # Close out all positions
        if self.position > 0:
            self.execute_trade(date, price, "SELL", self.position)

        # Compute final portfolio value
        data["net_wealth"] = portfolio_values
        returns = pd.Series(portfolio_values).pct_change().dropna()

        self.results = {
            "Final Balance": self.cash,
            "Final Net Wealth": data["net_wealth"].iloc[-1],
            "Performance (%)": ((data["net_wealth"].iloc[-1] - self.initial_cash) / self.initial_cash) * 100,
            "Total Trades": len(self.trades),
            "Position Size": data["Position Size"],
            "Sharpe Ratio": self.compute_sharpe_ratio(returns),
            "Sortino Ratio": self.compute_sortino_ratio(returns),
            "Max Drawdown": self.compute_max_drawdown(data["net_wealth"]),
        }

        if "Stop Loss Price" in data.columns:
            self.results["Stop Loss Price"] = data["Stop Loss Price"].ffill()
        else:
            logger.warning("No 'Stop Loss Price' found in strategy output. Stop-loss plot will be skipped.")
        
        self.results["net_wealth"] = data["net_wealth"].copy()
        return self.results

    def compute_sharpe_ratio(self, returns: pd.Series, risk_free_rate=0.01):
        return (returns.mean() - risk_free_rate) / returns.std() if returns.std() != 0 else np.nan

    def compute_max_drawdown(self, portfolio_values: pd.Series):
        drawdown = portfolio_values / portfolio_values.cummax() - 1
        return drawdown.min()

    def compute_sortino_ratio(self, returns: pd.Series, risk_free_rate=0.01):
        downside_returns = returns[returns < 0]
        return (returns.mean() - risk_free_rate) / downside_returns.std() if downside_returns.std() != 0 else np.nan

    @staticmethod
    def optimize_parameters(data: pd.DataFrame, strategy_class: Type[TradingStrategy], param_grid: Dict[str, list]) -> Tuple[Dict[str, float], Dict[str, any]]:
        """Runs Grid Search to optimize strategy parameters."""
        param_combinations = list(product(*param_grid.values()))
        best_performance = -float("inf")
        best_params = None
        best_results = None

        for params in param_combinations:
            strategy = strategy_class(**dict(zip(param_grid.keys(), params)))
            engine = BacktestEngine(strategy)
            results = engine.run_backtest(data.copy())
            performance = results["Performance (%)"]
            
            if performance > best_performance:
                best_performance = performance
                best_params = dict(zip(param_grid.keys(), params))
                best_results = results

        logger.info(f"Best parameters: {best_params} with {best_performance:.2f}% return")
        return best_params, best_results
