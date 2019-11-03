import backtrader as bt
import backtrader.feeds as btfeeds
import os
import datetime


class TestStrategy(bt.Strategy):
    """Sample to backtrade a strategy.

    1)Put your strategy in the method next()
    2)Put your data on variable datapath
    3)Run this file to see results

    Others parameters (amount of the account at first, stake of each trade, ...)
    can be change easily, see https://www.backtrader.com/ for more informations
    """
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f" %
                         (order.executed.price, order.executed.value,
                          order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log("SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f" %
                         (order.executed.price, order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" %
                 (trade.pnl, trade.pnlcomm))

    # The strategy:

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])

        if self.order:
            return

        if not self.position:

            if self.dataclose[0] - self.dataclose[-1] > 200:

                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()

        else:

            if self.dataclose[0] - self.dataclose[-1] < -200:
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    datapath = "./data/ETHUSDT_1HOUR_26_08_2019.csv"

    # Create a Data Feed
    data = btfeeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2018, 1, 1),
        dtformat=("%Y-%m-%d %H:%M:%S"),
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1,
        timeframe=bt.TimeFrame.Minutes,
        compression=30,
    )

    #Set up and lauch the backtrade
    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=0.05)
    cerebro.broker.setcommission(commission=0.00075)
    print("Starting Balance: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("Final Balance: %.2f" % cerebro.broker.getvalue())
    cerebro.plot()
    print()
