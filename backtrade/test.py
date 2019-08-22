from binance.client import Client

apiKey = "DKpYeQJDdxgo2mSXIqKnk70QmOy8urDQjJFjPDk06H4waWrj1irLnuFFfHpXMCcC"
secretKey = "PIp3AKATJfillNs9Lsm1pbUaTMQqMTXFfGS5H77DMwzi6a1GPLOyt78hv03kcf1f"

client = Client(apiKey, secretKey)

klines = client.get_historical_klines(
"BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC"
)
print(klines)