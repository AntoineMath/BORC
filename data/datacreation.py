import keys
import datetime
import pandas as pd
from time import sleep
from binance.client import Client

"""
data.py create a csv file with these informations :
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
"""

client = Client(keys.apiKey, keys.secretKey)

symbol = "BTCUSDT"

BTC_1min = client.get_historical_klines(
    symbol, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"
)

BTC_1min = pd.DataFrame(
    BTC_1min,
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

BTC_1min["Open time"] = pd.to_datetime(BTC_1min["Open time"], unit="ms")

BTC_1min.set_index("Open time", inplace=True)

BTC_1min.to_csv("BTC_1min_21_08_2019")

