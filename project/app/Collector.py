from abc import ABC, abstractmethod


class Collector(ABC):
    @abstractmethod
    def collect(self, start, stop):
        pass
