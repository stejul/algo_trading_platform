from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"

class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(str, Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class Order(BaseModel):
    order_id: str = Field(description="Unqique order identifier")
    symbol: str = Field(min_length=1, description="Stock Symbol e.g: AAPL, GOOGL")
    order_type = OrderType
    side: OrderSide
    quantity: float = Field(gt=0,description="Number of shares")
    price: Optional[float] = Field(None, ge=0, description="Order price (None for market orders)")
    status: OrderStatus = OrderStatus.PENDING
    timestamp: datetime = Field(default_factory = datetime.utcnow)

class Trade(BaseModel):
    trade_id: str = Field(description="Unique trade identifier")
    order_id: str = Field(description="Associated order ID")
    symbol: str
    quantity: float = Field(gt=0, description="Number of shares")
    price: float = Field(gt=0, description="Execution price per share")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MarketData(BaseModel):
    symbol: str
    timestamp: datetime
    open_price: float = Field(ge=0)
    high_price: float = Field(ge=0)
    low_price: float = Field(ge=0)
    close_price: float = Field(ge=0)
    volume: float = Field(ge=0)

class Portfolio(BaseModel):
    cash_balance: float = Field(ge=0, description="Available cash in account")
    holdings: Dict[str, float] = Field(default_factory=dict, description="Stock holdings {symbol: quantity}")

    def update_cash(self, amount: float):
        """Update cash balance after a trade."""
        self.cash_balance += amount

    def update_holdings(self, symbol: str, quantity: float):
        """Update holdings after a trade."""
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity

class StrategyConfig(BaseModel):
    name: str = Field(description="Strategy name")
    parameters: Dict[str, float] = Field(description="Configurable parameters")
