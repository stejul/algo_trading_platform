import pandas as pd
from src.application.market_data import MarketDataService
from src.domain.strategy import SMAStrategy, MomentumStrategy, MeanReversionStrategy, RSIStrategy
from src.application.backtesting import BacktestEngine
from src.application.risk_control import RiskControl
from src.infrastructure.logging import get_logger
from src.utils.visualization import TradingVisualizer

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting Algorithmic Trading Platform...")

    # Initialize Services
    market_data_service = MarketDataService()
    risk_manager = RiskControl()

    # Fetch Market Data
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    symbol = "AAPL"

    df = market_data_service.get_historical_data(symbol, start_date, end_date)
    logger.info(f"Market data fetched successfully: {df.shape[0]} rows")

    # Ensure timestamp column is in datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Select Strategy
    strategy = RSIStrategy(period=14, overbought=70, oversold=30)  # New RSI strategy
    strategy_name = strategy.__class__.__name__

    # Compute Indicators & Generate Signals
    df = strategy.compute_indicators(df)
    df["signal"] = df.apply(strategy.generate_signal, axis=1)
    logger.info(f"Generated {df['signal'].notna().sum()} trading signals")

    # Apply Risk Control (Stop Loss)
    df = risk_manager.apply_stop_loss(df)

    # Run Backtest
    engine = BacktestEngine(strategy)
    results = engine.run_backtest(df)

    # Ensure required fields exist in results
    if "Stop Loss Price" not in results:
        logger.warning("Skipping stop-loss plot: 'Stop Loss Price' column not found in backtest results.")
    if "Position Size" not in results:
        logger.warning("Skipping position sizing plot: 'Position Size' column not found in backtest results.")
    if "net_wealth" not in results or not isinstance(results["net_wealth"], pd.Series):
        logger.warning("Skipping drawdown plot: 'net_wealth' is missing or not a time series.")
    
    # Visualize Strategy-Specific Indicators
    TradingVisualizer.plot_candlestick_with_signals(df, df)
    if "Position Size" in results:
        TradingVisualizer.plot_position_sizing(pd.DataFrame({"timestamp": df["timestamp"], "Position Size": results["Position Size"]}))
    if "Stop Loss Price" in results:
        TradingVisualizer.plot_stop_loss_levels(df, pd.Series(results["Stop Loss Price"]))
    if "net_wealth" in results and isinstance(results["net_wealth"], pd.Series):
        TradingVisualizer.plot_drawdown(results["net_wealth"], max_drawdown=0.2)
    
    TradingVisualizer.plot_portfolio_value(pd.DataFrame({"timestamp": df["timestamp"], "net_wealth": results["net_wealth"]}))
    TradingVisualizer.print_backtest_results(results)

    logger.info("Trading run completed successfully.")
