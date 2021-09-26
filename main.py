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
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

# local imports
from gpwCollector import GpwDataLoader as gpwDL


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
    date_start = '04-01-2013'
    date_end = '26-09-2021'
    instr = 'CDPROJEKT'
    i_start = 26# 26 sie wysypało sprawdzic to 
    # i_stop =  27
    emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]

    collector = gpwDL(instr, date_start, date_end)
    collector.read_gpw_stock(instr)
    # collector.update_csv(instr + ".csv")
    # df  = gpwdt.collect_data(date_start, date_end, 'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=')
    # gpwdt.save_csv('WIG.csv', df, 'stock' )
    # print(gpwdt.save_csv.__doc__)
    # gpwdt.update_all_csv()
    # eng = SimulatorEngine('WIGpop.csv',10000)
    # eng.rs_rating()
    # wigScan = StocksScanner('WIGpop.csv')
    # wigScan.rs_rating()

    # bitScan = StocksScanner('company/11BIT.csv')
    # bitScan.rs_rating()

    # eng.calculate_ema(emas_used)
    # eng.make_plot()
    # eng.strategy()
    # eng.indicators()




if __name__ == '__main__':
    main()
