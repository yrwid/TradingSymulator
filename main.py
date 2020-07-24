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
        try:
            resp = req.get(
                'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=' 
                + instrument+'&date=' 
                + data
                )

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

        for i in range(1):   #len(gpw_stocks)):
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




class simulatorEngine():


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
                self.indktrs["gains"] += i
                self.indktrs["ng"] += 1
            else:
                self.indktrs["losses"] += i
                self.indktrs["nl"] += 1
            self.indktrs["total_r"] = self.indktrs["total_r"]*((prc/100)+1)

        self.indktrs["total_r"] = round((self.indktrs["total_r"]-1)*100,2)

        if(ng>0):
            self.indktrs["avg_gain"] = self.indktrs["gains"]/self.indktrs["ng"]
            self.indktrs["max_r"] = str(max(self.percent_change))
        else:
            self.indktrs["avg_gain"] = 0
            self.indktrs["max_r"] = "undefined"

        if(nl>0):
            self.indktrs["avg_loss"] = losses/nl
            self.indktrs["max_l"] = str(min(self.percent_change))
            self.indktrs["ratio"] = str(
                -self.indktrs["avg_gain"]/self.indktrs["avg_loss"])

        else:
            self.indktrs["avg_loss"] = 0 
            max_l="undefined"
            ratio="inf"

        if(ng>0 or nl>0):
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




def main():
    date_start = '01-01-2020'
    date_end = '16-07-2020'
    instr = 'CDPROJEKT'
    i_start = 26# 26 sie wysypało sprawdzic to 
    i_stop =  27
    emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]

    gpwdt = GpwDataLoader(instr,date_start,date_end)
    gpwdt.update_all_csv()
    # eng = simulatorEngine('11BIT.csv')
    # eng.calculate_ema(emas_used)
    # eng.make_plot()
    # gpwdt.read_gpw_stocks(date_start,date_end,i_start ,i_stop)




if __name__ == '__main__':
    main()
