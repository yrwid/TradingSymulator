from app.Engine import Engine
from app.Strategy import Strategy
from app.EngineExceptions import *
from datetime import datetime
import pandas as pd

class EngineImpl(Engine):
    def __init__(self, df):
        Engine.__init__(self, df)
        self.strategy = None
        self.working_df = None

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def run(self, start=None, stop=None):
        if start is not None and stop is not None:
            self.working_df = self.__cut_df_to(start, stop)
        else:
            self.working_df = self.df


    def get_current_run_data(self):
        pass

    def __cut_df_to(self, start: datetime, stop: datetime) -> pd.DataFrame:
        start_pos = self.__get_indexes(start.strftime("%Y-%b-%d"))
        stop_pos = self.__get_indexes(stop.strftime("%Y-%b-%d"))

        if len(start_pos) != 1 or len(stop_pos) != 1:
            raise RedundantEdgeData

        self.working_df = self.df.iloc[start_pos[0][0]:stop_pos[0][0], :]


    def __get_indexes(self, value):
        list_of_pos = []
        result = self.df.isin([value])
        series_obj = result.any()
        column_names = list(series_obj[series_obj == True].index)

        for col in column_names:
            rows = list(result[col][result[col] == True].index)

            for row in rows:
                list_of_pos.append((row, col))

        return list_of_pos
