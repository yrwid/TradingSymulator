import backtrader as bt
import math

class GoldenCross(bt.Strategy):
    params = (('fast', 5), ('slow', 15), ('order_percentage', 0.95),('ticker' ,'NAME'))

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            period = self.params.fast, plotname = ' 5 day moving average ' 
        )

        self.slow_moving_average = bt.indicators.SMA(
            period = self.params.slow, plotname = ' 15 day moving average ' 
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average,self.slow_moving_average)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amout_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amout_to_invest / self.data.close)

                print("BUY {} shares of {} at {}".format(self.size,self.params.ticker,self.data.close[0]))
               # self.log('DATA{}'.format(self.dataclose[0]))

                self.buy(size = self.size)

        if self.position.size > 0:
            if self.crossover < 0: 
                print("SELL {} shares of {} at {}".format(self.size,self.params.ticker,self.data.close[0]))
                self.close()



class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))
            self.bar_executed = len(self)

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) == (self.bar_executed + 5):
                self.log('SELL CREATED {}'.format(self.dataclose[0]))
                self.order = self.sell()
