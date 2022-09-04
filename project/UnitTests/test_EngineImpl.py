from app.EngineImpl import EngineImpl
from app.DataManagerImpl import DataManagerImpl
from datetime import datetime
from app.EngineDTO import EngineDTO
from app.Strategy import Strategy
from app import EngineExceptions
import pytest

# You can see which side it is better to start creating class

class StrategyBasedOnDays(Strategy):
    def __init__(self, stocks_bought_already: bool):
        Strategy.__init__(self, stocks_bought_already)

    def calculate(self, dto: EngineDTO):
        self.date = dto.date
        # Buy at first day of every month
        if self.date.day == 1:
            self._buy_if_possible()

        # Sell on 7th day of month
        if self.date.day == 7:
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
            buy_result = (self.previousClosePrices[i].price < self.previousClosePrices[i+1].price) \
                          and self.previousClosePrices[i].initialized and buy_result
        buy_result = dto.currentClosePrice > self.previousClosePrices[len(self.previousClosePrices) - 1].price and buy_result

        for i in range(len(self.previousClosePrices) - 1):
            sell_result = (self.previousClosePrices[i].price > self.previousClosePrices[i+1].price) \
                           and self.previousClosePrices[i].initialized and sell_result
        sell_result = dto.currentClosePrice < self.previousClosePrices[len(self.previousClosePrices) - 1].price and sell_result

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
    def __init__(self, stocks_bought_already: bool):
        Strategy.__init__(self, stocks_bought_already)

    def calculate(self, dto: EngineDTO):
        self.date = dto.date

        if dto.ema20 is None or dto.ema5 is None:
            return

        if dto.ema20 > dto.ema5:
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
    expected_buy_signals = (datetime(2021, 8, 17), datetime(2021, 9, 6))
    expected_sell_signals = (datetime(2021, 8, 20), datetime(2021, 9, 22))

    assert buy_sell_signals["signals"]["buy"] == expected_buy_signals
    assert buy_sell_signals["signals"]["sell"] == expected_sell_signals


def test_buy_sell_signals_basad_on_days(engine_with_data):
    based_on_days_test_strategy = StrategyBasedOnDays(stocks_bought_already=False)
    eng = engine_with_data
    eng.set_strategy(based_on_days_test_strategy)
    buy_sell_signals = eng.run()
    expected_buy_signals = (datetime(2021, 9, 1), datetime(2021, 10, 1))
    expected_sell_signals = (datetime(2021, 9, 7), datetime(2021, 10, 7))

    assert buy_sell_signals["signals"]["buy"] == expected_buy_signals
    assert buy_sell_signals["signals"]["sell"] == expected_sell_signals


def test_buy_sell_signals_basad_on_emas(engine_with_data):
    ema_based_test_strategy = StrategyBasedOnEmaData(stocks_bought_already=False)
    eng = engine_with_data
    eng.set_strategy(ema_based_test_strategy)
    buy_sell_signals = eng.run()

    expected_buy_signals = (datetime(2021, 9, 8),)
    expected_sell_signals = (datetime(2021, 9, 30),)

    print(buy_sell_signals["emas"]["20"])
    assert buy_sell_signals["signals"]["buy"] == expected_buy_signals
    assert buy_sell_signals["signals"]["sell"] == expected_sell_signals


def test_inconsistency_date():
    ema_based_test_strategy = StrategyBasedOnEmaData(stocks_bought_already=False)
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", "goldFiles/cdproject_incosistency_data.csv", "csv")
    eng = EngineImpl(data_manager.get_df())
    eng.set_strategy(ema_based_test_strategy)

    with pytest.raises(EngineExceptions.InconsistencyData):
        eng.run()


def test_exceptions(engine_with_data):
    ema_based_test_strategy = StrategyBasedOnEmaData(stocks_bought_already=False)
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", "goldFiles/cdproject_exception_data.csv", "csv")
    eng = EngineImpl(data_manager.get_df())
    eng.set_strategy(ema_based_test_strategy)

    with pytest.raises(EngineExceptions.EdgeDateNotExist):
        eng.run(datetime(2021, 8, 28))

    with pytest.raises(EngineExceptions.RedundantEdgeData):
        eng.run(datetime(2021, 8, 31))
