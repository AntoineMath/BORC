import sys, os
import strategy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import data.keys

pair1 = 'BTC'
pair2 = 'USDT'
amount_to_trade = 3

strategy.__trade__(data.keys.apiKey, data.keys.secretKey, pair1, pair2, amount_to_trade)
