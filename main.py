import datetime as dt
from src.application.market_data import MarketDataService
#from src.application.execution import ExecutionService
#from src.domain.strategy import MovingAverageStrategy  # Example strategy
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting Algorithmic Trading Platform...")

    # Initialize Services
    market_data_service = MarketDataService()
    #execution_service = ExecutionService()

    # Fetch Market Data
    start_date = "2000-01-01"
    end_date = dt.date.today().strftime("%Y-%m-%d")
    symbol = "AAPL"

    df = market_data_service.get_historical_data(symbol, start_date, end_date)
    logger.info(f"Market data fetched successfully: {df.shape[0]} rows")

    # Initialize Strategy
    #strategy = MovingAverageStrategy()

    # Run Strategy
    #signals = strategy.generate_signals(df)
    #logger.info(f"Generated {len(signals)} trading signals")

    # Execute Trades
    #for signal in signals:
        #execution_service.execute_trade(signal)

    logger.info("Trading run completed successfully.")
