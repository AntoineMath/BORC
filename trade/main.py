import sys, os
from time import sleep
import datetime
from binance.client import Client
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import data.keys

client = Client(data.keys.apiKey, data.keys.secretKey)

print(client)
