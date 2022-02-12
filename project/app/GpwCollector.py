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
        return self.__collect_data_from_period(start, stop)


    def __collect_data_from_period(self, date_start, date_end):
        start = dt.strptime(date_start, '%Y-%m-%d')
        stop = dt.strptime(date_end, '%Y-%m-%d')

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
        for i in range(len(df)):
            data_time_object = dt.strptime(df.iloc[i, 1], '%d-%m-%Y')
            df.iloc[i, 1] = data_time_object.strftime('%Y-%m-%d')

        lines_to_drop = list()
        for i in range(len(df)):
            if df.iloc[i, 2] is 'no data':
                lines_to_drop.append(i)

        df = df.drop(labels=lines_to_drop, axis=0)
        df = df.drop(['Name', 'ISIN', 'Currency', 'VolumeInQuantity', 'AmountOfDeals'], axis=1)
        df = df[["Date", "Open", "Close", "Max", "Min", "Volume(mln. PLN)", "Change(%)"]]

        col = ["Open", "Close", "Max", "Min", "Volume(mln. PLN)", "Change(%)"]

        df[col] = df[col].astype(float)
        df['Volume(mln. PLN)'] = round(df['Volume(mln. PLN)']/1000, 2)

        df = df[::-1]
        df.reset_index(drop=True, inplace=True)
        return df
