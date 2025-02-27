import yfinance as yf
from datetime import datetime
from typing import List, Optional
from src.domain.models import MarketData
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)

def fetch_historical_data(symbol: str, start_date: str, end_date: Optional[str] = None) -> List[MarketData]:
    """
    Fetches historical market data for a given symbol.
    
    :param symbol: Stock ticker (e.g., "AAPL").
    :param start_date: Start date in "YYYY-MM-DD" format.
    :param end_date: End date in "YYYY-MM-DD" format (optional, defaults to today).
    :return: List of MarketData objects.
    """
    logger.info(f"Fetching data for {symbol} from {start_date} to {end_date}")

    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)

        market_data_list = []
        for timestamp, row in df.iterrows():
            market_data = MarketData(
                symbol=symbol,
                timestamp=datetime.utcfromtimestamp(timestamp.timestamp()),
                open_price=row["Open"],
                high_price=row["High"],
                low_price=row["Low"],
                close_price=row["Close"],
                volume=row["Volume"]
            )
            market_data_list.append(market_data)

        logger.info(f"Successfully retrieved data for {symbol}")
        return market_data_list
    except Exception as e:
        logger.error(f"Error fetching data for symbol {symbol}: {e}")
