from app.DataController import *

class CsvDataController(DataController):
    @abstractmethod
    def __init__(self, stock_name):
        self.stock_name = stock_name

    @abstractmethod
    def erase(self, data_frame):
        pass

    @abstractmethod
    def append(self, data_frame):
        pass

    @abstractmethod
    def read(self):
        pass
