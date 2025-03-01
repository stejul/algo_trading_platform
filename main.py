import pandas as pd
from src.application.market_data import MarketDataService
from src.domain.strategy import SMAStrategy, MomentumStrategy, MeanReversionStrategy
from src.application.backtesting import BacktestEngine
from src.infrastructure.logging import get_logger
from src.utils.visualization import TradingVisualizer

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting Algorithmic Trading Platform...")

    # Initialize Services
    market_data_service = MarketDataService()

    # Fetch Market Data
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    symbol = "AAPL"

    df = market_data_service.get_historical_data(symbol, start_date, end_date)
    logger.info(f"Market data fetched successfully: {df.shape[0]} rows")

    # Ensure timestamp column is in datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Select Strategy
    strategy = SMAStrategy(short_window=50, long_window=200)
    strategy_name = strategy.__class__.__name__

    # Compute Indicators & Generate Signals
    df = strategy.compute_indicators(df)
    df["signal"] = df.apply(strategy.generate_signal, axis=1)
    logger.info(f"Generated {df['signal'].notna().sum()} trading signals")

    # Run Backtest
    engine = BacktestEngine(strategy)
    results = engine.run_backtest(df)

    # Visualize Strategy-Specific Indicators
    TradingVisualizer.plot_candlestick_with_signals(df, df)
    TradingVisualizer.plot_strategy_indicators(df, strategy_name)
    TradingVisualizer.plot_portfolio_value(pd.DataFrame({"timestamp": df["timestamp"], "net_wealth": df["close_price"]}))
    TradingVisualizer.print_backtest_results(results)

    logger.info("Trading run completed successfully.")
