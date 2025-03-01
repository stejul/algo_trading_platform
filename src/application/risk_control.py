import pandas as pd
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)

class RiskControl:
    """ Implements basic risk management techniques for trading. """

    def __init__(self, max_drawdown: float = 0.2, risk_per_trade: float = 0.02, stop_loss_pct: float = 0.05):
        """
        :param max_drawdown: Maximum allowable portfolio drawdown (e.g., 20% means stop trading if loss exceeds 20%).
        :param risk_per_trade: Percentage of total capital risked per trade (e.g., 2%).
        :param stop_loss_pct: Fixed stop loss as percentage of trade price (e.g., 5%).
        """
        self.max_drawdown = max_drawdown
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pct = stop_loss_pct
        self.initial_capital = None
        self.current_capital = None
        logger.info("RiskControl initialized with max_drawdown=%.2f, risk_per_trade=%.2f, stop_loss_pct=%.2f", 
                    max_drawdown, risk_per_trade, stop_loss_pct)

    def initialize_capital(self, initial_capital: float):
        """ Sets the initial trading capital. """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        logger.info("Initial capital set to %.2f", initial_capital)

    def check_drawdown(self) -> bool:
        """ Returns True if max drawdown is exceeded, stopping trading. """
        drawdown_exceeded = self.current_capital / self.initial_capital < (1 - self.max_drawdown)
        if drawdown_exceeded:
            logger.warning("Max drawdown exceeded! Trading should stop.")
        return drawdown_exceeded

    def calculate_position_size(self, trade_price: float) -> int:
        """ Determines position size based on risk per trade. """
        capital_at_risk = self.current_capital * self.risk_per_trade
        position_size = capital_at_risk / (trade_price * self.stop_loss_pct)
        logger.info("Calculated position size: %d for trade price: %.2f", position_size, trade_price)
        return int(position_size)

    def apply_stop_loss(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Applies stop loss levels to the dataset. """
        data["Stop Loss Price"] = data["close_price"] * (1 - self.stop_loss_pct)
        logger.info("Stop loss applied to dataset")
        return data

    def update_capital(self, trade_profit_loss: float):
        """ Updates capital after a trade is completed. """
        self.current_capital += trade_profit_loss
        logger.info("Updated capital: %.2f after trade profit/loss: %.2f", self.current_capital, trade_profit_loss)
