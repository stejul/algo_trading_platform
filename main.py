from src.infrastructure.data.yfinance import fetch_historical_data
from src.infrastructure.persistence import ParquetWriter, CsvWriter, JsonWriter
from src.domain.models import MarketData
import datetime as dt
import pandas as pd


if __name__ == "__main__":
    start_date = "2000-01-01"
    end_date = dt.date.today()

    data = fetch_historical_data(symbol = "AAPL", start_date = start_date, end_date = end_date)
    data_dicts = [entry.model_dump() for entry in data]
    data = pd.DataFrame(data = data_dicts, columns=["symbol", "timestamp", "open_price", "high_price", "low_price", "close_price", "volume"])
    print(data.head(10))
    par_wri = ParquetWriter()
    par_wri.write(data = data, destination="historical_data/test.parquet")
