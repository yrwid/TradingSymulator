from app.EngineImpl import EngineImpl
from app.EngineDTO import EngineDTO
from app.Strategy import Strategy
from datetime import datetime


# You can see which side it is better to start creating class

class TestStrategy(Strategy):
    def __init__(self):
        self.buy_signal = list()
        pass

    def calculate(self, date: datetime, dto: EngineDTO):
        # Buy at first day of every month
        if date.day == 1:
            self.buy_signal.append(date)

        # TODO: Create signals base on data.

    def get_indicators(self):
        pass


def test_set_strategy():
    test_strategy = TestStrategy()
    eng = EngineImpl()
    result = eng.set_strategy(test_strategy)


def test_run_engine():
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