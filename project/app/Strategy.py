from abc import ABC, abstractmethod
from datetime import datetime
from app.EngineDTO import EngineDTO


class Strategy(ABC):
    def __init__(self, stocks_bought_already: bool):
        self.buy_signals = list()
        self.sell_signals = list()
        self.isBoughtAlready = stocks_bought_already
        self.date = None

    @abstractmethod
    def calculate(self, dto: EngineDTO):
        pass

    def get_indicators(self):
        return {"buy": tuple(self.buy_signals), "sell": tuple(self.sell_signals)}

    def _buy_if_possible(self):
        if self.isBoughtAlready is False:
            self.buy_signals.append(self.date)
            self.isBoughtAlready = True

    def _sell_if_possible(self):
        if self.isBoughtAlready is True:
            self.sell_signals.append(self.date)
            self.isBoughtAlready = False
