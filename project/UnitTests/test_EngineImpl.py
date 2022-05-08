from app.EngineImpl import EngineImpl
from app.DataManagerImpl import DataManagerImpl
from datetime import datetime
from app.EngineDTO import EngineDTO
from app.Strategy import Strategy
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


class TestStrategyBasedOnEmaData(Strategy):
    def calculate(self, date: datetime, dto: EngineDTO):
        self.date = date

        if dto.ema15 > dto.ema5:
            self._sell_if_possible()
        else:
            self._buy_if_possible()


class TestStrategyBasedOnPriceData(Strategy):
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

# based on price
# 2021-08-18 - Buy
# 2021-08-24 - sell
# 2021-09-08 - buy
# 2021-09-24 - sell

def test_buy_sell_signals(engine_with_data):
    test_strategy = TestStrategyBasedOnEmaData(stocks_bought_alredy=False)
    eng = engine_with_data
    eng.set_strategy(test_strategy)


def test_inconsistency_date():
    pass


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