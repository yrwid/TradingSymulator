from abc import ABC, abstractmethod
from app.Strategy import Strategy

class Engine(ABC):
    @abstractmethod
    def set_strategy(self, strategy: Strategy):
        pass

    @abstractmethod
    def run(self, start, stop):
        pass
