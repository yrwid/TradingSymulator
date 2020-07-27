# -----------------------------------------------------------
# Poland stocks market symaulator private project, 
# include data loader and technical strategies 
#  
#
# (C) 2020 Dawid Mudry, Tychy, Poland
# Released under GNU Public License (GPL)
# email: mudri656@gmail.com
# -----------------------------------------------------------

# TO DO:
# Finish stocks scanner class.  
# Add docstrings to methods. 
# Implement abstract class  in strategy class. 
# Implement green line breakout.
# Do something with indicators (more reusable code).  
# Expand abstract class (??).
# Create IBD Realative strength indicator. 
# Implement WIG index function.
# Better plots (more reusable code).
# Fix forward loop in GpwDataLoader class.

import requests as req
import bs4
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import date
import time
from abc import ABC, abstractmethod

class GpwDataLoader:

    def __init__(self, instrument, date_start,date_end):
        self.instrument = instrument
        self.date_start = date_start
        self.date_end = date_end




    def __arch_stocks(self, instrument, data):
        """Calculate the sum of value1 and value2."""
        try:
            resp = req.get(
                'https://www.gpw.pl/archiwum-notowan-full?type=1&instrument=' 
                + instrument+'&date=' 
                + data
                )
            print(resp)
            soup = bs4.BeautifulSoup(resp.text, "xml")
            table_footable = soup.find_all(
                'table',
                {'class' : 'table footable'}
                )

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

        return arch_stats




    def save_csv(self, path, df):
        """Calculate the sum of value1 and value2."""
        for i in range(len(df)):
            if(df.iloc[i,2] == 'no data' and i != 0 ):
                df.iloc[i,[2,3,7]] = df.iloc[i-1,[2,3,7]]

            elif(i == 0):
                for j in range(130): # to fix in future 
                    if(df.iloc[j,2] != 'no data'):
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
            [str(start_date) , str(date.today().strftime('%d-%m-%Y') )]
            )

        df = self.collect_data(update_dates[0], update_dates[1])

        for i in range(len(df)):
            if(df.iloc[i,2] == 'no data' and i != 0 ):
                df.iloc[i,[2,3,7]] = df.iloc[i-1,[2,3,7]]

            elif(i == 0):
                df.iloc[i,2] = temp_tuple[2] 
                df.iloc[i,3] = temp_tuple[3]
                df.iloc[i,7] = temp_tuple[7]
        df.to_csv(path, mode='a', header=False, index = False)




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




    def collect_data(self, date_start, date_end):
        start = dt.strptime(date_start, '%d-%m-%Y')
        stop = dt.strptime(date_end, '%d-%m-%Y')
        delta = timedelta(days=1) 
        df = pd.DataFrame([])
        tmp = list()

        while start <= stop:
            print("Downloading {} data... ".format(start.date()))
            stats = self.__arch_stocks(
                self.instrument,
                start.strftime('%d-%m-%Y')
                )

            tmp.append(stats)
            start = start + delta # increase day one by one
            print("Done.")
            
        df = pd.DataFrame(tmp,columns=[
            'Name','data','ISIN','currency','openV',
            'maxV','minV','closeV','valueChagPer',
            'vol','amountOfDeals','valueOfDeals']
            )

        col = [
            'openV','maxV','minV','closeV',
            'valueChagPer','vol','amountOfDeals','valueOfDeals'
            ]

        df[col] = df[col].astype(float,errors = 'ignore')
        return df




    def read_gpw_stocks(self, date_start, date_end, i_start, i_stop):
        excel_gpw_stocks = 'gpwStocks.xlsx'
        gpw_stocks = pd.read_excel(excel_gpw_stocks, index_col=False)

        for i  in range(i_start,i_stop): #(len(gpw_stocks))
            print('Now: {}'.format(str(gpw_stocks.iloc[i,0])))
            company_name = gpw_stocks.iloc[i,0]  # 11bit-studio ISIN
            self.instrument = company_name
            df = self.collect_data(date_start, date_end)
            self.save_csv(str(gpw_stocks.iloc[i,0]) + '.csv',df)



    #funckja sciągająca psuje poprawić 
    def get_wig(self):
        self.instrument = 'WIG1'
        # df = self.collect_data(self.date_start, self.date_end)
        df = pd.read_csv('WIG.csv')

        for i in range(len(df)):
            for j in range(11,3,-1):
                # print("------------------")
                # print(df.iloc[i, j])
                # print(df.iloc[i, j-1] )
                # print("------------------")
                df.iloc[i, j] = df.iloc[i, j-1] 
            df.iloc[i,3] = 'index'
        
        for i in range(len(df)):
            if(df.iloc[i,5] == 'no data' and i != 0 ):
                df.iloc[i, 7] = df.iloc[i-1, 7]

            elif(i == 0):
                df.iloc[i, 7] = df.iloc[i+1, 7]

        self.save_csv('WIGpop.csv',df)




    def update_wig(self):
        self.update_csv('company/wig.csv')
         
#--------------------------------------------------------------------------------------------------------------------------------------------


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

#--------------------------------------------------------------------------------------------------------------------------------------------


class SimulatorEngine():


    def __init__(self, path, cash):
        self.path = path
        self.__data = self.__read_csv()
        self.cash = cash




    def __read_csv(self):
        df = pd.read_csv(self.path)
        df.closeV = pd.to_numeric(df.closeV)
        return df




    def calculate_sma(self, windows):
        self.__data['MA'+str(win)] = self.__data['closeV'].rolling(window=win).mean()
        return True




    def calculate_ema(self, emas_used):
        self.emas_used = emas_used
        for x in emas_used:
            ema = x
            self.__data['EMA'+str(ema)] = round(
                self.__data['closeV'].ewm(span=ema,adjust=False).mean(),
                2
                )

        return True




    def make_plot(self):
        cv=['closeV']
        for ema in self.emas_used:
            cv.append('EMA'+str(ema))
        self.__data.plot(x ='data', y=cv, kind = 'line',marker = '.')
        plt.show()
        return True




    def strategy(self):
        pos = 0
        num = 0
        self.percent_change = list()

        for i in self.__data.index:
            cmin = min( 
                    self.__data['EMA5'][i], self.__data['EMA8'][i],
                    self.__data['EMA10'][i],self.__data['EMA12'][i],
                    self.__data['EMA15'][i]
                    )  

            cmax = max(
                    self.__data['EMA30'][i],self.__data['EMA35'][i],
                    self.__data['EMA40'][i],self.__data['EMA45'][i],
                    self.__data['EMA50'][i],self.__data['EMA60'][i]
                    )

            close = self.__data['closeV'][i] 

            if(cmin > cmax):
                if(pos == 0):
                    bp = close
                    pos = 1
                    print('Buying at {}, data:{} '.format(
                        bp,
                        self.__data['data'][i]
                        )
                    )

            elif(cmin < cmax):
                if(pos == 1):
                    sp = close
                    pos = 0
                    print('selling at {}, data:{} '.format(
                        sp,
                        self.__data['data'][i]
                        )
                    )

                    pc = (sp/bp - 1)*100
                    self.percent_change.append(pc)

            if(num == self.__data['closeV'].count()-1 and pos == 1):
                pos = 0
                sp = close
                print('executing sell at end of data, price: {}, data:{}'.format(
                    sp,
                    self.__data['data'][i]
                    )
                )

                pc = (sp/bp - 1)*100
                self.percent_change.append(pc)

            num+=1

        return True




    def indicators(self):
        self.indktrs = {
                "gains" : 0,
                "ng" : 0,
                "losses" : 0,
                "nl" : 0,
                "total_r" : 1,
                "avg_gain": 0,
                "max_r": 0,
                "avg_loss": 0,
                "max_l": 0,
                "ratio": 0,
                "batting_avg": 0
            }  

        for prc in self.percent_change:
            if(prc>0):
                self.indktrs["gains"] += prc
                self.indktrs["ng"] += 1
            else:
                self.indktrs["losses"] += prc
                self.indktrs["nl"] += 1
            self.indktrs["total_r"] = self.indktrs["total_r"]*((prc/100)+1)

        self.indktrs["total_r"] = round((self.indktrs["total_r"]-1)*100,2)

        if(self.indktrs["ng"]>0):
            self.indktrs["avg_gain"] = self.indktrs["gains"]/self.indktrs["ng"]
            self.indktrs["max_r"] = str(max(self.percent_change))
        else:
            self.indktrs["avg_gain"] = 0
            self.indktrs["max_r"] = "undefined"

        if(self.indktrs["nl"] > 0):
            self.indktrs["avg_loss"] = self.indktrs["losses"]/self.indktrs["nl"]
            self.indktrs["max_l"] = str(min(self.percent_change))
            self.indktrs["ratio"] = str(
                -self.indktrs["avg_gain"]/self.indktrs["avg_loss"])

        else:
            self.indktrs["avg_loss"] = 0 
            max_l = "undefined"
            ratio = "inf"

        if(self.indktrs["ng"] > 0 or self.indktrs["nl"] > 0):
            self.indktrs["batting_avg"] = self.indktrs["ng"]/(self.indktrs["ng"]+
                self.indktrs["nl"]
                )

        else:
            self.indktrs["batting_avg"] = 0

        print()
        print(
            "Results for stocks going back to " 
            + str(self.__data['data'][0])+", Sample size: " 
            + str(self.indktrs["ng"]+self.indktrs["nl"]) + " trades"
            )
            
        print("EMAs used: " + str(self.emas_used))
        print("Batting Avg: " + str(self.indktrs["batting_avg"]))
        print("Gain/loss ratio: " + self.indktrs["ratio"])
        print("Average Gain: " + str(self.indktrs["avg_gain"]))
        print("Average Loss: " + str(self.indktrs["avg_loss"]))
        print("Max Return: " + self.indktrs["max_r"])
        print("Max Loss: " + self.indktrs["max_l"])
        print(
            "Total return over "  
            + str(self.indktrs["ng"] + self.indktrs["nl"])  
            + " trades: "  
            + str(self.indktrs["total_r"]) + "%" 
            )
        print()

        return self.indktrs

#--------------------------------------------------------------------------------------------------------------------------------------------


class StocksScanner():
    
    def __init__(self, path):
        self.path = path
        self.__data = self.__read_csv()
    
    def calculate_stock_rs_rating(self):
        # rs_stck = rs_rating(stck_path)
        # rs_wig = rs_rating(wig_path)
        pass


    def rs_rating(self): 
        close_0 = self.__data.iloc[-1]['closeV'] #current close value
        close_m64 = self.__data.iloc[-64]['closeV']
        close_m128 = self.__data.iloc[-128]['closeV']
        close_m189 = self.__data.iloc[-189]['closeV']

        # in the end 256, now 206 because first verse is no data: 01.01.2020
        close_m256 = self.__data.iloc[-206]['closeV']  

        print(close_0,close_m64,close_m128,close_m256)
        # normilized 
        # rs_rt = (((close_0 - close_m64)/close_m64)*0.4 
            # + ((close_0 - close_m128)/close_m128)*0.2   
            # + ((close_0 - close_m189)/close_m189)*0.2  
            # + ((close_0 - close_m256)/close_m256)*0.2)*100  # in range 0-100

        rs_rt = ((close_0/close_m64)*0.4 
            + (close_0/close_m128)*0.2   
            + (close_0/close_m189)*0.2  
            + (close_0/close_m256)*0.2)*100  # in range 0-100
        print(rs_rt)

        return rs_rt




    def __read_csv(self):
        df = pd.read_csv(self.path)
        df.closeV = pd.to_numeric(df.closeV)
        return df




    def calculate_sma(self, data, windows):
        data['MA'+str(win)] = data['closeV'].rolling(window=win).mean()
        return data




    def scan_all(self):
        excel_gpw_stocks = 'gpwStocks.xlsx'
        gpw_stocks = pd.read_excel(excel_gpw_stocks, index_col=False)

        for i  in range(i_start,i_stop): #(len(gpw_stocks))
            print('Now: {}'.format(str(gpw_stocks.iloc[i,0])))
            company_name = gpw_stocks.iloc[i,0]  
            self.path = 'campany/' + company_name
            df = self.__read_csv()

            # calulate SMA 150 days and 200 days 
            df = self.calculate_sma(df,150)
            df = self.calculate_sma(df,200)

#--------------------------------------------------------------------------------------------------------------------------------------------



def main():
    date_start = '01-01-2020'
    date_end = '27-07-2020'
    instr = 'CDPROJEKT'
    i_start = 26# 26 sie wysypało sprawdzic to 
    # i_stop =  27
    emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]

    # gpwdt = GpwDataLoader(instr,date_start,date_end)
    # gpwdt.get_wig()
    # print(gpwdt.save_csv.__doc__)
    # gpwdt.update_all_csv()
    # eng = SimulatorEngine('WIGpop.csv',10000)
    # eng.rs_rating()
    wigScan = StocksScanner('WIGpop.csv')
    wigScan.rs_rating()

    bitScan = StocksScanner('company/11BIT.csv')
    bitScan.rs_rating()

    # eng.calculate_ema(emas_used)
    # eng.make_plot()
    # eng.strategy()
    # eng.indicators()




if __name__ == '__main__':
    main()
