# -----------------------------------------------------------
# Interface for any strategy class.
#  
#
# (C) 2021 Dawid Mudry, Tychy, Poland
# Released under GNU Public License (GPL)
# -----------------------------------------------------------

from abc import ABC, abstractmethod
import pandas as pd

class AbcEngine(ABC):

    def __init__(self, path, cash):
        self.path = path
        self.__data = self.__read_csv()
        self.cash = cash
   

    def __read_csv(self):
        df = pd.read_csv(self.path)
        df.closeV = pd.to_numeric(df.closeV)
        return df


    @abstractmethod
    def strategy(self):
        pass


    @abstractmethod
    def make_plot(self):
        pass
    

    @abstractmethod
    def indicators(self):
        pass