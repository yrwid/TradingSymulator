from app.EngineImpl import EngineImpl
from app.DataManagerImpl import DataManagerImpl
from datetime import datetime
from app.EngineDTO import EngineDTO
from app.Strategy import Strategy
from app import EngineExceptions
import pytest

# You can see which side it is better to start creating class

class StrategyBasedOnDays(Strategy):
    def calculate(self, dto: EngineDTO):
        self.date = dto.date
        # Buy at first day of every month
        if self.date.day == 1:
            self._buy_if_possible()

        # Sell on 25th day of month
        if self.date.day == 25:
            self._sell_if_possible()


class StrategyBasedOnPriceOverTimeData(Strategy):
    class PreviousPriceType:
        def __init__(self, price, init):
            self.price = price
            self.initialized = init

    def __init__(self, stocks_bought_already: bool):
        Strategy.__init__(self, stocks_bought_already)
        self.previousClosePrices = [self.PreviousPriceType(0.0, False) for _ in range(3)]

    def calculate(self, dto: EngineDTO):
        self.date = dto.date

        buy_result = True
        sell_result = True
        for i in range(len(self.previousClosePrices) - 1):
            buy_result = (self.previousClosePrices[i] < self.previousClosePrices[i+1]) and buy_result

        for i in range(len(self.previousClosePrices) - 1):
            sell_result = (self.previousClosePrices[i] > self.previousClosePrices[i+1]) and sell_result


        if buy_result == True and sell_result == True:
            raise RuntimeError("sell and buy signals occurred at the same time")

        if sell_result:
            self._sell_if_possible()
        if buy_result:
            self._buy_if_possible()

        for i in range(len(self.previousClosePrices)):
            if i+1 >= len(self.previousClosePrices):
                self.previousClosePrices[i].price = dto.currentClosePrice
                self.previousClosePrices[i].initialized = True
            else:
                # TODO: find better way to copy objects :D
                self.previousClosePrices[i].price = self.previousClosePrices[i+1].price
                self.previousClosePrices[i].initialized = self.previousClosePrices[i + 1].initialized


class StrategyBasedOnEmaData(Strategy):
    def calculate(self, dto: EngineDTO):
        self.date = dto.date

        if dto.ema15 > dto.ema5:
            self._sell_if_possible()
        else:
            self._buy_if_possible()


@pytest.fixture()
def engine_with_data():
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", "goldFiles/cdprojectEngineTestMalformedData.csv", "csv")
    df = data_manager.get_df()
    eng = EngineImpl(df)
    yield eng


def test_buy_sell_signals_basad_on_price(engine_with_data):
    price_over_time_test_strategy = StrategyBasedOnPriceOverTimeData(stocks_bought_already=False)
    eng = engine_with_data
    eng.set_strategy(price_over_time_test_strategy)
    buy_sell_signals = eng.run()
    expected_buy_signals = (datetime(2021, 8, 17), datetime(2020, 9, 8))
    expected_sell_signals = (datetime(2020, 8, 24), datetime(2020, 9, 24))

    assert buy_sell_signals["signals"]["buy"] == expected_buy_signals
    assert buy_sell_signals["signals"]["sell"] == expected_sell_signals


def test_buy_sell_signals_basad_on_days(engine_with_data):
    based_on_days_test_strategy = StrategyBasedOnDays(stocks_bought_already=False)
    eng = engine_with_data
    eng.set_strategy(based_on_days_test_strategy)
    buy_sell_signals = eng.run()
    expected_signals = ((datetime(2021, 8, 25), False),
                        (datetime(2020, 9, 1), True),
                        (datetime(2020, 10, 1),  True))

    assert buy_sell_signals == expected_signals


def test_buy_sell_signals_basad_on_emas(engine_with_data):
    ema_based_test_strategy = StrategyBasedOnEmaData(stocks_bought_already=False)
    eng = engine_with_data
    eng.set_strategy(ema_based_test_strategy)
    buy_sell_signals = eng.run()
    expected_signals = ((datetime(2021, 8, 18), False),
                        (datetime(2020, 9, 3), True),
                        (datetime(2020, 9, 29),  False))

    assert buy_sell_signals == expected_signals


def test_inconsistency_date():
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", "goldFiles/cdproject_incosistency_data.csv", "csv")
    eng = EngineImpl(data_manager.get_df())
    with pytest.raises(EngineExceptions.InconsistencyData):
        eng.run()


def test_exceptions():
    assert False
    