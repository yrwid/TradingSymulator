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
        supported_emas_in_days = (5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60)

        self.working_df = self.__cut_df_if_necessary_to(start, stop)
        self.__calculate_emas_indicators(supported_emas_in_days)
        self.run_strategy()
        self.strategy.get_indicators()
        # return sell/buy indicators and emas/price data

    # def get_current_run_data(self):
    #     pass

    def __cut_df_if_necessary_to(self, start: datetime, stop: datetime) -> pd.DataFrame:
        if start is not None and stop is not None:
            start_pos = self.__get_indexes(start.strftime("%Y-%b-%d"))
            stop_pos = self.__get_indexes(stop.strftime("%Y-%b-%d"))

            # TODO: Split these checks into two separated methods each checking only one position.
            if len(start_pos) > 1 or len(stop_pos) > 1:
                raise RedundantEdgeData

            if len(start_pos) < 1 or len(stop_pos) < 1:
                raise EdgeDateNotExist

        elif start is not None and stop is None:
            start_pos = self.__get_indexes(start.strftime("%Y-%b-%d"))

            if len(start_pos) > 1:
                raise RedundantEdgeData

            if len(start_pos) < 1:
                raise EdgeDateNotExist

        elif start is None and stop is not None:
            stop_pos = self.__get_indexes(stop.strftime("%Y-%b-%d"))

            if len(stop_pos) > 1:
                raise RedundantEdgeData

            if len(stop_pos) < 1:
                raise EdgeDateNotExist

        else:
            return self.df

        return self.df.iloc[start_pos[0][0]:stop_pos[0][0], :]

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

    def __calculate_emas_indicators(self, emas):
        pass

    def __calculate_ema(self, days, smoothing=2):
        prices = self.working_df["Close"]
        ema = [sum(prices[:days]) / days]
        for price in prices[days:]:
            ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
        return ema
