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


def __trade__(api_key, secret_key, pair1, pair2, amount_to_trade):
    logging.basicConfig(filename="trade.log",
                        level=logging.INFO,
                        format='%(asctime)s: %(message)s')
    TIME_START = datetime.datetime.now()
    client = Client(api_key, secret_key)
    logging.info("START")
    last_trade = "hodl"
    start = True

    while True:

        value = float(
            client.get_order_book(symbol=pair1 + pair2)['bids'][0][0])

        if last_trade == "buy" or start == True:

            if simulation.__algo_simulation__(value) == 0:

                if float(client.get_asset_balance(asset=pair1)['free']) < amount_to_trade/value:

                    amount_to_trade = round(float(client.get_asset_balance(asset=pair1)['free'], 4))

                start = False
                algo_side = "sell"
                order = client.order_market_sell(symbol=pair1 + pair2, quantity=round(amount_to_trade/value, 4))
                logging.info("sell BTC to have USDT")

        if  last_trade == "sell" or start == True:

            if simulation.__algo_simulation__(value) == 2:

                if float(client.get_asset_balance(asset=pair2)['free']) < amount_to_trade:

                    amount_to_trade = round(float(client.get_asset_balance(asset=pair1)['free'], 4))

                start = False
                algo_side = "buy"
                order = client.order_market_buy(symbol=pair1 + pair2, quantity=round(amount_to_trade/value, 4))
                logging.info("buy BTC against USDT")

        sleep(2)


__trade__(data.keys.apiKey, data.keys.secretKey, 'BTC', 'USDT', 3)