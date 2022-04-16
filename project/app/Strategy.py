from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def calculate(self, date, data):
        pass

    @abstractmethod
    def get_indicators(self):
        pass