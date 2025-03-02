# Algorithmic Trading Platform

## Overview
This is a modular algorithmic trading platform that supports multiple trading strategies, backtesting, and performance analysis. It allows traders and quantitative researchers to develop, test, and optimize strategies efficiently.

## Features
- **Multiple Trading Strategies**: SMA Crossover, Momentum, Mean Reversion, RSI
- **Technical Indicators**: ATR, MACD, Bollinger Bands
- **Backtesting Engine**: Simulates historical trading performance
- **Risk Management**: Stop-loss and drawdown monitoring
- **Performance Metrics**: Sharpe Ratio, Sortino Ratio, Max Drawdown
- **Visualization**: Candlestick charts, equity curve comparison, returns distribution

## Installation
### Prerequisites
- Python 3.9+
- `uv` package manager (recommended for dependency management)

### Setup Instructions
1. **Clone the Repository**:

2. **Install `uv` Package Manager** (if not installed):
   ```bash
   pip install uv
   ```

3. **Create and Activate a Virtual Environment**:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage
### Running the Backtesting Engine
To run the platform and test different strategies, execute:
```bash
python main.py
```

### Adding New Strategies
1. Create a new class in `strategy.py` that extends `TradingStrategy`.
2. Implement `compute_indicators()` and `generate_signal()` methods.
3. Register the strategy in `main.py` under the `strategies` dictionary.

### Running Tests ***WIP***
To verify the implementation:
```bash
pytest tests/
```

## Project Structure
```
├── notebooks/
├── cache/
├── logs/
├── src/
│   ├── application/
│   │   ├── backtesting.py
│   │   ├── market_data.py
│   │   ├── risk_control.py
│   │   ├── execution.py
│   ├── domain/
│   │   ├── strategy.py
│   │   ├── models.py
│   │   ├── risk.py
│   ├── infrastructure/
│   │   ├── broker/
│   │   │   ├─  ...
│   │   ├── data/
│   │   │   ├─  yfinance.py
│   │   ├── persistence/
│   │   │   ├─  data_writer.py
│   │   │   ├─  csv_writer.py
│   │   │   ├─  db_writer.py
│   │   │   ├─  parquet_writer.py
│   │   │   ├─  json_writer.py
│   │   ├── logging.py
│   │   ├── config.py
│   ├── utils/
│   │   ├── visualization.py
│   ├── interfaces/
│   │   ├── cli.py
├── tests/
├── main.py
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── README.md
├── LICENSE.md
├── .env

### ENV Variables
```
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

DEFAULT_DATA_SOURCE=yfinance
YFINANCE_CACHE=True

ALPHA_VANTAGE_API_KEY=your_alphavantage_key_here #can be empty
BINANCE_API_KEY=your_binance_key_here # can be empty

DB_URL=sqlite:///data/trading.db

CACHE_ENABLED=True
CACHE_EXPIRATION_DAYS=3
CACHE_DIR=cache/

LOG_FILE_PATH=logs/trading_platform.log
```


## License
[MIT License](LICENSE)


