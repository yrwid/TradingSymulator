from app.Collector import *
from app.GpwCollectorExceptions import *
import requests as req
import bs4
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'


class GpwCollector(Collector):
    def __init__(self):
        self.INSTRUMENT_TYPES = {'stock': 'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument='}
        self.instrument = None
        self.instrument_type = None

    def set_stock(self, stock_name):
        self.instrument = stock_name
        self.instrument_type = self.INSTRUMENT_TYPES['stock']

    def collect(self, start, stop):
        if self.instrument is None:
            raise StockNameNotExist("Uninitialized stock name, run set_stock() method first")

        try:
            start = dt.strptime(start, '%Y-%m-%d')
            stop = dt.strptime(stop, '%Y-%m-%d')
        except ValueError:
            raise WrongStartDate("Wrong start ot stop date")

        current_datetime = dt.datetime.today()
        bottom_acceptable_date = current_datetime - dt.timedelta(days=5000)

        # if (start > bottom_acceptable_date)
        # print(bottom_acceptable_date)

        return self.__collect_data_from_period(start, stop)

    def __collect_data_from_period(self, date_start, date_end):


        period_data = self.__iterate_and_collect_throughth(start, stop)
        df = self.__create_data_frame_from(period_data)
        df = self.__adjust_data(df)

        return df

    def __iterate_and_collect_throughth(self, start, stop):
        data_from_period = list()
        while start <= stop:
            one_day_data = self.__collect_one_record_from(start.strftime('%d-%m-%Y'))
            data_from_period.append(one_day_data)
            start += timedelta(days=1)  # increase day one by one

        return data_from_period

    def __collect_one_record_from(self, date):
        try:
            page = self.__send_page_request(date)
            historical_stock_data = self.__scrap_data_from(page)
        except IndexError:
            historical_stock_data = self.__mark_date_as_market_closed(date)

        return historical_stock_data

    def __send_page_request(self, date):
        return req.get(self.instrument_type
                       + self.instrument
                       + '&date=' + date)

    def __scrap_data_from(self, page):
        soup = bs4.BeautifulSoup(page.text, "xml")
        table_footable = soup.find_all('table', {'class': 'table footable'})
        tr_tag = table_footable[0].find_all('tr')
        table = tr_tag[1].text.replace(",", ".").replace(" ", "")
        table_strings = list(map(lambda x: x.strip(), table.split("\n")))
        stock_data = [string for string in table_strings if string]

        return stock_data

    def __mark_date_as_market_closed(self, date):
        return [self.instrument, date, 'no data', 'no data', 'no data',
                'no data', 'no data', 'no data', 'no data', 'no data',
                'no data', 'no data']

    def __create_data_frame_from(self, data):
        return pd.DataFrame(data,
                        columns=['Name', 'Date', 'ISIN', 'Currency', 'Open',
                                 'Max', 'Min', 'Close', 'Change(%)',
                                 'VolumeInQuantity', 'AmountOfDeals', 'Volume(mln. PLN)'])

    def __adjust_data(self, df):
        df_with_flipped_date = self.__flip_date_in_data_frame(df)
        df_without_market_closed_rows = self.__drop_market_closed_rows(df_with_flipped_date)
        df_with_need_only_data = self.__drop_unused_data(df_without_market_closed_rows)
        df_sorted = self.__sort_columns_to_match(df_with_need_only_data)
        df_with_numeric_columns = self.__convert_to_float(["Open", "Close", "Max",
                                                           "Min", "Volume(mln. PLN)", "Change(%)"],
                                                           df_sorted)
        df_with_numeric_columns['Volume(mln. PLN)'] = round(df_with_numeric_columns['Volume(mln. PLN)']/1000, 2)
        reversed_df = self.__reverse_data_frame_upside_down(df_with_numeric_columns)
        final_df_outcome = reversed_df.reset_index(drop=True)

        return final_df_outcome

    def __flip_date_in_data_frame(self, df):
        for i in range(len(df)):
            data_time_object = dt.strptime(df.iloc[i, 1], '%d-%m-%Y')
            df.iloc[i, 1] = data_time_object.strftime('%Y-%m-%d')

        return df

    def __drop_market_closed_rows(self, df):
        lines_to_drop = list()
        for i in range(len(df)):
            if df.iloc[i, 2] is 'no data':
                lines_to_drop.append(i)
        df = df.drop(labels=lines_to_drop, axis=0)

        return df

    def __drop_unused_data(self, df):
        return df.drop(['Name', 'ISIN', 'Currency', 'VolumeInQuantity', 'AmountOfDeals'], axis=1)

    def __sort_columns_to_match(self, df):
        return df[["Date", "Open", "Close", "Max", "Min", "Volume(mln. PLN)", "Change(%)"]]

    def __convert_to_float(self, list_of_columns, df):
        df[list_of_columns] = df[list_of_columns].astype(float)
        return df

    def __reverse_data_frame_upside_down(self, df):
        return df[::-1]