import datetime as dt
from src.application.market_data import MarketDataService
#from src.application.execution import ExecutionService
from src.domain.strategy import SMAStrategy# Example strategy
from src.infrastructure.logging import get_logger
from src.utils.visualization import TradingVisualizer

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
    strategy = SMAStrategy(short_window = 50, long_window=200)

    # Run Strategy
    signals = strategy.generate_signals(df)
    logger.info(f"Generated {len(signals)} trading signals")

    # Execute Trades
    #for signal in signals:
        #execution_service.execute_trade(signal)
    print("Signals")
    print(signals[["timestamp", "close_price", "signal"]].head(10))
    print("DF")
    print(df.head(10))

    indicators = {
        "SMA Short": "SMA_Short",
        "SMA Long": "SMA_Long",
        "Momentum": "momentum",
        "Rolling Mean": "rolling_mean",
        "Upper Band": "upper_band",
        "Lower Band": "lower_band",
    }

    # Remove unused indicators
    indicators = {k: v for k, v in indicators.items() if v in signals.columns}
    
    TradingVisualizer.plot_candlestick_with_signals(signals[signals["timestamp"] >= "2024-01-01"])
    TradingVisualizer.plot_indicators(signals, indicators, title="Trading Strategy Visualization")

    logger.info("Trading run completed successfully.")
