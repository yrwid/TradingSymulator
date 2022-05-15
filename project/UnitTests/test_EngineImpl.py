from app.EngineImpl import EngineImpl
from app.DataManagerImpl import DataManagerImpl
from datetime import datetime
from app.EngineDTO import EngineDTO
from app.Strategy import Strategy
from app import EngineExceptions
import pytest

# You can see which side it is better to start creating class

class TestStrategyBasedOnDays(Strategy):
    def calculate(self, date: datetime, dto: EngineDTO):
        self.date = date
        # Buy at first day of every month
        if date.day == 1:
            self._buy_if_possible()

        # Sell on 25th day of month
        if date.day == 25:
            self._sell_if_possible()



class TestStrategyBasedOnPriceOverTimeData(Strategy):
    class PreviousPriceType:
        price: float
        active: bool

    def __init__(self, stocks_bought_already: bool):

        Strategy.__init__(self, stocks_bought_already)
        self.previousClosePrices = [self.PreviousPriceType() for _ in range(4)]

    def calculate(self, date: datetime, dto: EngineDTO):
        self.date = date

        buy_result = True
        sell_result = True
        for previousPrice in self.previousClosePrices:
            if not (previousPrice.price < dto.currentClosePrice and buy_result and previousPrice.active):
                buy_result = False;

            if not (previousPrice.price > dto.currentClosePrice and sell_result and previousPrice.active)
                sell_result = False

        if buy_result == sell_result:
            raise RuntimeError("sell and buy signals occurred at the same time")

        if sell_result:
            self._sell_if_possible()
        if buy_result:
            self._buy_if_possible()

        for i in range(len(self.previousClosePrices)):
            if i+1 >= len(self.previousClosePrices):
                self.previousClosePrices[i] = dto.currentClosePrice
            else:
                self.previousClosePrices[i] = self.previousClosePrices[i+1]


class TestStrategyBasedOnEmaData(Strategy):
    def calculate(self, date: datetime, dto: EngineDTO):
        self.date = date

        if dto.ema15 > dto.ema5:
            self._sell_if_possible()
        else:
            self._buy_if_possible()


@pytest.fixture()
def engine_with_data():
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", "goldFiles/cdprojectEngineTestMalformedData.csv", "csv")
    eng = EngineImpl(data_manager.get_df())
    yield eng


# Based on ema5 and ema15
# 2021-08-18 - sell
# 2021-09-03 - buy
# 2021-09-29 - sell

# based on price over time
# 2021-08-18 - Buy
# 2021-08-24 - sell
# 2021-09-08 - buy
# 2021-09-24 - sell

#based on days
# 2021-08-25 - sell
# 2021-09-01 - buy
2021-10-01 - buy

def test_buy_sell_signals(engine_with_data):
    price_over_time_test_strategy = TestStrategyBasedOnPriceOverTimeData(stocks_bought_already=False)
    eng = engine_with_data
    eng.set_strategy(price_over_time_test_strategy)
    buy_sell_signals = eng.run()
    expected_signals = ((datetime(2021, 8, 18), True),
                        (datetime(2020, 8, 24), False),
                        (datetime(2020, 9, 8),  True),
                        (datetime(2020, 9, 24), False))

    assert buy_sell_signals == expected_signals

    based_on_days_test_strategy = TestStrategyBasedOnDays(stocks_bought_already=False)
    eng.set_strategy(based_on_days_test_strategy)
    buy_sell_signals = eng.run()
    expected_signals = ((datetime(2021, 8, 25), False),
                        (datetime(2020, 9, 1), True),
                        (datetime(2020, 10, 1),  True))

    assert buy_sell_signals == expected_signals

    ema_based_test_strategy = TestStrategyBasedOnEmaData(stocks_bought_already=False)
    eng.set_strategy(ema_based_test_strategy)
    buy_sell_signals = eng.run()
    expected_signals = ((datetime(2021, 8, 18), False),
                        (datetime(2020, 9, 3), True),
                        (datetime(2020, 9, 29),  False))

    assert buy_sell_signals == expected_signals

def test_inconsistency_date():
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", "cdproject_incosistency_data.csv", "csv")
    eng = EngineImpl(data_manager.get_df())
    with pytest.raises(EngineExceptions.InconsistencyData):
        eng.run()


def test_wrong_input_date():
    pass


def test_input_indicators():
    pass


def test_correct_buy_signals():
    pass


def test_correct_sell_signas():
    pass


def test_exceptions():
    pass