from abc import ABC, abstractmethod


class Collector(ABC):
    @abstractmethod
    def set_stock(self, stock_name):
        pass

    @abstractmethod
    def collect(self, start, stop):
        pass


