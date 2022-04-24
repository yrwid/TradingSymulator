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


class TestStrategyBasedOnData(Strategy):
    def calculate(self, date: datetime, dto: EngineDTO):
        self.date = date
        cmin = min(dto.ema5, dto.ema8, dto.ema10, dto.ema12, dto.ema15)
        cmax = max(dto.ema30, dto.ema35, dto.ema40, dto.ema45, dto.ema50, dto.ema60)

        if cmin > cmax:
            self._buy_if_possible()
        elif cmin < cmax:
            self._sell_if_possible()

@pytest.fixture()
def engine_with_data():
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", "goldFiles/cdproject.csv", "csv")
    test_strategy = TestStrategyBasedOnDays()
    eng = EngineImpl(data_manager.get_df())
    eng.set_strategy(test_strategy)

def test_buy_sell_signals():
    pass


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