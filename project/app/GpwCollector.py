from Collector import *
from GpwCollectorExceptions import *
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

    def __collect_one_record_from(self, date):
        try:
            resp = req.get(
                self.instrument_type
                + self.instrument
                + '&date=' + date
            )

            soup = bs4.BeautifulSoup(resp.text, "xml")
            table_footable = soup.find_all(
                'table',
                {'class': 'table footable'})

            tr = table_footable[0].find_all('tr')
            table = tr[1].text.replace(",", ".").replace(" ", "")
            table_strings = list(map(lambda x: x.strip(), table.split("\n")))
            arch_stats = [string for string in table_strings if string]

        except IndexError as not_opened_stock_market:
            print("Exeption occured")
            arch_stats = [
                self.instrument, date, 'no data', 'no data', 'no data',
                'no data', 'no data', 'no data', 'no data', 'no data',
                'no data', 'no data']

        if len(arch_stats) == 11:
            arch_stats.insert(3, 'index')

        return arch_stats

    def collect_data_from_period(self, date_start, date_end):
        start = dt.strptime(self.date_start, '%Y-%m-%d')
        stop = dt.strptime(self.date_end, '%Y-%m-%d')
        delta = timedelta(days=1)
        df = pd.DataFrame([])
        retrieved_data_temporary = list()

        while start <= stop:
            print("Downloading {} data... ".format(start.date()))
            stats = self.__collect_one_record_from(start.strftime('%d-%m-%Y'))
            retrieved_data_temporary.append(stats)
            start = start + delta  # increase day one by one
            print("Done.")

        df = pd.DataFrame(retrieved_data_temporary, columns=[
            'Name', 'data', 'ISIN', 'currency', 'openV',
            'maxV', 'minV', 'closeV', 'valueChagPer',
            'vol', 'amountOfDeals', 'valueOfDeals'])

        col = [
            'openV', 'maxV', 'minV', 'closeV',
            'valueChagPer', 'vol', 'amountOfDeals', 'valueOfDeals']

        df[col] = df[col].astype(float, errors='ignore')
        return df
