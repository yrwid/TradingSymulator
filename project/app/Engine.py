from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def set_strategy(self, stock_name):
        pass

    @abstractmethod
    def run(self, start, stop):
        pass
