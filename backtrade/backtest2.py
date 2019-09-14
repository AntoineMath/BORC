import backtrader as bt
import backtrader.feeds as btfeeds
import os, sys
import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from trade.simulation import __algo_simulation__
import argparse


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        starting_price = self.dataclose[1]
        final_price = self.dataclose[0]
        diff_price = starting_price - final_price
        percentage_diff_price = 100 * (-diff_price / starting_price)

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

            if __algo_simulation__("price") == 0:

                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()

        else:

            if __algo_simulation__("price") == 2:
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Benchmark/TimeReturn Observers Sample')

    parser.add_argument('--timeframe',
                        required=False,
                        action='store',
                        default=None,
                        choices=TIMEFRAMES.keys(),
                        help=('TimeFrame to apply to the Observer'))

    # Plot options
    parser.add_argument('--plot',
                        '-p',
                        nargs='?',
                        required=False,
                        metavar='kwargs',
                        const=True,
                        help=('Plot the read data applying any kwargs passed\n'
                              '\n'
                              'For example:\n'
                              '\n'
                              '  --plot style="candle" (to plot candles)\n'))

    if pargs:
        return parser.parse_args(pargs)

    return parser.parse_args()


TIMEFRAMES = {
    None: None,
    'days': bt.TimeFrame.Days,
    'weeks': bt.TimeFrame.Weeks,
    'months': bt.TimeFrame.Months,
    'years': bt.TimeFrame.Years,
    'notimeframe': bt.TimeFrame.NoTimeFrame,
}


def run_strat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    datapath = os.path.abspath(os.getcwd() +
                               "/data/ETHUSDT_1HOUR_26_08_2019.csv")

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

    cerebro.adddata(data)

    cerebro.broker.setcash(1000.0)

    cerebro.addsizer(bt.sizers.FixedSize, stake=0.05)

    cerebro.broker.setcommission(commission=0.00075)

    starting_balance = cerebro.broker.getvalue()

    cerebro.addobserver(bt.observers.Benchmark,
                        data=data,
                        timeframe=bt.TimeFrame.NoTimeFrame)

    #Run the backtarde
    results = cerebro.run()

    final_balance = cerebro.broker.getvalue()
    diff_balance = 100 * (final_balance - starting_balance) / starting_balance

    print("Starting Balance: %.2f" % starting_balance)
    print("Final Balance: %.2f" % final_balance)
    print("Profit: %.2f " % diff_balance + "%")

    cerebro.plot()


if __name__ == "__main__":
    run_strat()