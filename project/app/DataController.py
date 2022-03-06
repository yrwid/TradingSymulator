from abc import ABC, abstractmethod


class DataController(ABC):
    @abstractmethod
    def erase(self):
        pass

    @abstractmethod
    def append(self, data_frame):
        pass

    @abstractmethod
    def read(self):
        pass
