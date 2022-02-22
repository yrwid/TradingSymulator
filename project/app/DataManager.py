from abc import ABC, abstractmethod

# comment 1: if we first think about tests we can spot additional interfaces.

class DataManager(ABC):
    @abstractmethod
    def __init__(self, stock_name):
        self.stock_name = stock_name

    @abstractmethod
    def get_most_recent_date(self):
        pass

    @abstractmethod
    def update(self, data_frame):
        pass

    @abstractmethod
    def read(self, start, stop):
        pass
