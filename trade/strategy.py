import sys
import os
from time import sleep
import datetime
from binance.client import Client
import simulation
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import data.keys
from simulation import __algo_simulation__
from binance.websockets import BinanceSocketManager
import logging


def __trade__(api_key, secret_key):
    logging.basicConfig(filename="info.log", level=logging.DEBUG)
    TIME_START = datetime.datetime.now()
    CLIENT = Client(api_key, secret_key)
    logging.info("aya")


print(__trade__(data.keys.apiKey, data.keys.secretKey))