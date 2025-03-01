import pandas as pd
from src.application.market_data import MarketDataService
from src.domain.strategy import SMAStrategy, MomentumStrategy, MeanReversionStrategy, RSIStrategy, TechnicalIndicators
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

    # Compute Technical Indicators
    df = TechnicalIndicators.compute_atr(df)
    df = TechnicalIndicators.compute_macd(df)
    df = TechnicalIndicators.compute_bollinger_bands(df)

    # Define Strategies
    strategies = {
        "SMA": SMAStrategy(short_window=20, long_window=50),
        "Momentum": MomentumStrategy(lookback=14),
        "Mean Reversion": MeanReversionStrategy(window=10),
        "RSI": RSIStrategy(period=14, overbought=70, oversold=30),
    }

    results = {}

    # Run Backtests
    for name, strategy in strategies.items():
        logger.info(f"Running backtest for {name}")
        df = strategy.compute_indicators(df)
        df["signal"] = df.apply(strategy.generate_signal, axis=1)
        df = risk_manager.apply_stop_loss(df)
        
        engine = BacktestEngine(strategy)
        results[name] = engine.run_backtest(df)
        
        logger.info(
            f"{name} Results: Performance={results[name]['Performance (%)']:.2f}%, "
            f"Sharpe Ratio={results[name].get('Sharpe Ratio', 'N/A'):.2f}, "
            f"Sortino Ratio={results[name].get('Sortino Ratio', 'N/A'):.2f}, "
            f"Max Drawdown={results[name].get('Max Drawdown', 'N/A'):.2f}"
        )
    
    # Visualizations
    TradingVisualizer.plot_candlestick_with_signals(df, df)
    TradingVisualizer.plot_sharpe_ratio(results)
    TradingVisualizer.plot_sortino_ratio(results)
    TradingVisualizer.plot_max_drawdown(results)
    TradingVisualizer.plot_equity_curve_comparison(results)
    TradingVisualizer.plot_returns_distribution(results)
    
    rsi_results = results.get("RSI", {})
    if "Position Size" in rsi_results:
        TradingVisualizer.plot_position_sizing(pd.DataFrame({"timestamp": df["timestamp"], "Position Size": rsi_results["Position Size"]}))
    if "Stop Loss Price" in rsi_results:
        TradingVisualizer.plot_stop_loss_levels(df, pd.Series(rsi_results["Stop Loss Price"]))
    if "net_wealth" in rsi_results and isinstance(rsi_results["net_wealth"], pd.Series):
        TradingVisualizer.plot_drawdown(rsi_results["net_wealth"], max_drawdown=0.2)
    
    if "net_wealth" in rsi_results:
        TradingVisualizer.plot_portfolio_value(pd.DataFrame({"timestamp": df["timestamp"], "net_wealth": rsi_results["net_wealth"]}))
    TradingVisualizer.print_backtest_results(rsi_results)

    logger.info("Trading run completed successfully.")
