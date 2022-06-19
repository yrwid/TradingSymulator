from abc import ABC, abstractmethod
from datetime import datetime
from app.Strategy import Strategy

class Engine(ABC):
    def __init__(self, df):
        self.df = df

    @abstractmethod
    def set_strategy(self, strategy: Strategy):
        pass

    @abstractmethod
    def run(self, start: datetime, stop: datetime):
        pass
