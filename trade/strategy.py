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
    client = Client(api_key, secret_key)
    logging.info("START")
    last_trade = "hodl"
    start = True
    amount_start = amount_to_trade

    while True:

        value = float(
            client.get_order_book(symbol=pair1 + pair2)['bids'][0][0])

        if last_trade == "buy" or start == True:

            if simulation.__algo_simulation__(value) == 2:

                if float(client.get_asset_balance(
                        asset=pair1)['free']) < amount_to_trade / value:

                    amount_to_trade = round(
                        float(
                            client.get_asset_balance(asset=pair1)['free'], 4))

                start = False
                last_trade = "sell"
                '''order = client.order_market_sell(symbol=pair1 + pair2,
                                                 quantity=round(
                                                     amount_to_trade / value,
                                                     4))'''
                logging.info(
                    str(round(amount_to_trade / value, 4)) + " " + pair1 +
                    " sold for " + pair2)
                amount_to_trade = amount_start

                trade_price = client.get_my_trades(symbol=pair1 +
                                                   pair2)[-1]['price']
                trade_quoteQty = client.get_my_trades(symbol=pair1 +
                                                      pair2)[-1]['quoteQty']
                print(
                    str(datetime.datetime.now()) + ", SELL EXECUTED, Price: " +
                    str(trade_price) + ", Cost: " + str(trade_quoteQty))

        if last_trade == "sell" or start == True:

            if simulation.__algo_simulation__(value) == 0:

                if float(client.get_asset_balance(
                        asset=pair2)['free']) < amount_to_trade:

                    amount_to_trade = round(
                        float(
                            client.get_asset_balance(asset=pair1)['free'], 4))

                start = False
                last_trade = "buy"
                '''order = client.order_market_buy(symbol=pair1 + pair2,
                                                quantity=round(
                                                    amount_to_trade / value,
                                                    4))'''

                logging.info(
                    str(round(amount_to_trade / value, 4)) + " " + pair1 +
                    " bought against " + pair2)
                amount_to_trade = amount_start

                trade_price = client.get_my_trades(symbol=pair1 +
                                                   pair2)[-1]['price']
                trade_quoteQty = client.get_my_trades(symbol=pair1 +
                                                      pair2)[-1]['qty']
                print(
                    str(datetime.datetime.now()) + ", BUY EXECUTED, Price: " +
                    str(trade_price) + ", Cost: " + str(trade_quoteQty))

        sleep(1)


logging.info("END")

if __name__ == "__main__":

    __trade__(data.keys.apiKey, data.keys.secretKey, 'BTC', 'USDT', 3)