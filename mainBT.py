import backtrader
import datetime as d
from strategies import GoldenCross

cerebro = backtrader.Cerebro()
cerebro.broker.set_cash(1000000)

print('Str port: %.2f' % cerebro.broker.getvalue())

# Create a data feed
data = backtrader.feeds.YahooFinanceData(dataname='orc_data.csv',
    fromdate=d.datetime(2000, 1, 1),
    todate=d.datetime(2000, 12, 31))

cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(GoldenCross)
cerebro.addsizer(backtrader.sizers.FixedSize, stake = 1000)
cerebro.run()

print('Str port: %.2f' % cerebro.broker.getvalue())

cerebro.plot()