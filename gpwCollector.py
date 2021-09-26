import requests as req
import bs4
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
import time
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

class GpwDataLoader:
    def __init__(self, instrument, date_start, date_end):
        self.instrument = instrument
        self.date_start = date_start
        self.date_end = date_end
        self.INSTRUMENT_TYPE_STOCK = 'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument='


    def __arch_stocks(self, instrument, data, instrument_type):
        try:
            resp = req.get(
                instrument_type 
                + instrument+'&date=' 
                + data
                )

            soup = bs4.BeautifulSoup(resp.text, "xml")
            table_footable = soup.find_all(
                'table',
                {'class' : 'table footable'})

            tr = table_footable[0].find_all('tr')
            table  = tr[1].text.replace(",",".").replace(" ","")
            table_strings = list(map(lambda x: x.strip(), table.split("\n")))
            arch_stats = [string for string in table_strings if string]

        except IndexError as e:
            
            print("Exeption occured")
            arch_stats = [
                instrument,data,'no data','no data','no data',
                'no data','no data','no data','no data','no data'
                ,'no data','no data'
                ]
   
        if len(arch_stats) == 11:
            arch_stats.insert(3,'index')

        return arch_stats

    def save_csv(self, path, df):
        for i in range(len(df)):
            if(df.iloc[i,2] == 'no data' and i != 0 ):
                df.iloc[i,[2,3,7]] = df.iloc[i-1,[2,3,7]]

            elif(i == 0 and df.iloc[i,2] == 'no data'):
                for j in range(130): # to fix in future 
                    if(df.iloc[j,2] != 'no data'):
                        print(j)
                        df.iloc[0,[2,3,7]] = df.iloc[j,[2,3,4]]
                        break

        df.closeV = pd.to_numeric(df.closeV)
        df.to_csv(path, index = False) 

    def update_csv(self, path):
        with open(path, "r") as f1:
            last_line = f1.readlines()[-1]
        
        temp_tuple = tuple(item for item in last_line.split(","))

        start_date = (
            (dt.strptime(temp_tuple[1], '%d-%m-%Y') + timedelta(days=1)).date()
            ).strftime('%d-%m-%Y')

        update_dates = list(
            [str(start_date) , str(date.today().strftime('%d-%m-%Y') )])

        self.date_start = update_dates[0]
        self.date_end = update_dates[1]
        df = self.collect_data(self.instrument, self.INSTRUMENT_TYPE_STOCK)

        for i in range(len(df)):
            if(df.iloc[i,2] == 'no data' and i != 0 ):
                df.iloc[i, [2, 3, 7]] = df.iloc[i-1, [2, 3, 7]]

            elif(i == 0):
                df.iloc[i, 2] = temp_tuple[2]
                df.iloc[i, 3] = temp_tuple[3]
                df.iloc[i, 7] = temp_tuple[7]
        df.to_csv(path, mode='a', header=False, index = False)

    # Not used yet 
    def update_all_csv(self):
        excel_gpw_stocks = 'gpwStocks.xlsx'
        path = 'company/'
        gpw_stocks = pd.read_excel(excel_gpw_stocks, index_col=False) 

        for i in range(len(gpw_stocks)):
            print("###### {} #######".format(i))
            company_name = gpw_stocks.iloc[i,0]  # 11bit-studio ISIN
            self.instrument = company_name
            self.update_csv(path + str(gpw_stocks.iloc[i,0] + '.csv'))
        
        return True

    def collect_data(self, instrument, instrument_type):
        start = dt.strptime(self.date_start, '%d-%m-%Y')
        stop = dt.strptime(self.date_end, '%d-%m-%Y')
        delta = timedelta(days=1) 
        df = pd.DataFrame([])
        tmp = list()

        while start <= stop:
            print("Downloading {} data... ".format(start.date()))
            stats = self.__arch_stocks(
                instrument,
                start.strftime('%d-%m-%Y'),
                instrument_type 
                )

            tmp.append(stats)
            start = start + delta # increase day one by one
            print("Done.")
        print(tmp)
        df = pd.DataFrame(tmp,columns=[
            'Name','data','ISIN','currency','openV',
            'maxV','minV','closeV','valueChagPer',
            'vol','amountOfDeals','valueOfDeals']
            )

        col = [
            'openV','maxV','minV','closeV',
            'valueChagPer','vol','amountOfDeals','valueOfDeals']

        df[col] = df[col].astype(float, errors = 'ignore')
        return df

    def read_gpw_stock(self, instrument):
        df = self.collect_data(instrument, self.INSTRUMENT_TYPE_STOCK)
        self.save_csv(self.instrument + '.csv', df)
        
    # Not used untill gpwStocks.xlsx will be resurrected to live :D 
    def read_gpw_stocks(self, date_start, date_end, i_start, i_stop):
        excel_gpw_stocks = 'gpwStocks.xlsx'
        gpw_stocks = pd.read_excel(excel_gpw_stocks, index_col=False)

        for i  in range(i_start,i_stop): #(len(gpw_stocks))
            print('Now: {}'.format(str(gpw_stocks.iloc[i,0])))
            company_name = gpw_stocks.iloc[i,0]  # 11bit-studio ISIN
            self.instrument = company_name
            df = self.collect_data(date_start, date_end, 'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=')
            self.save_csv(str(gpw_stocks.iloc[i,0]) + '.csv', df, 'stock')