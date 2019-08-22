import keys
import datetime
import pandas as pd
from time import sleep
from binance.client import Client

CLIENT = Client(keys.apiKey, keys.secretKey)
CSV_NAME = "BTCUSDT_1MIN_22_08_2019.csv"

DATA_TO_CSV = CLIENT.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 year ago UTC"
)

DATA_TO_CSV = pd.DataFrame(
    DATA_TO_CSV,
    columns=[
        "Open time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
        "Ignore",
    ],
)
DATA_TO_CSV.rename(
    columns={
        "Open time": "open_time",
        "Open": "open",
        "High": "high", 
        "Low": "low", 
        "Close": "close",
        "Volume": "volume",
        "Close time": "close_time",
        "Quote asset volume": "quote_asset_volume",
        "Number of trades": "number_of_trades",
        "Taker buy base asset volume": "taker_buy_base_asset_volume",
        "Taker buy quote asset volume": "taker_buy_quote_asset_volume",
        "Ignore": "ignore"}, inplace=True
)
DATA_TO_CSV["open_time"] = pd.to_datetime(DATA_TO_CSV["open_time"], unit="ms")

DATA_TO_CSV.set_index("open_time", inplace=True)

DATA_TO_CSV.to_csv(CSV_NAME)
