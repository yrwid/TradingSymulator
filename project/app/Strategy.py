from abc import ABC, abstractmethod
from datetime import datetime
from app.EngineDTO import EngineDTO

class Strategy(ABC):
    def __init__(self):
        self.buy_signals = list()
        self.sell_signals = list()
        self.isBoughtAlready = False
        self.date = ""

    @abstractmethod
    def calculate(self, date: datetime, dto: EngineDTO):
        pass

    def get_indicators(self):
        return {"Buy": tuple(self.buy_signals), "Sell": tuple(self.sell_signals)}

    def _buy_if_possible(self):
        if self.isBoughtAlready is False:
            self.buy_signals.append(self.date)
            self.isBoughtAlready = True

    def _sell_if_possible(self):
        if self.isBoughtAlready is True:
            self.sell_signals.append(self.date)
            self.isBoughtAlready = False
