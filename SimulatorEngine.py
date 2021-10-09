# -----------------------------------------------------------
# Poland stocks market symaulator private project, 
# include data loader and technical strategies. 
#
# Keep in mind this class is To Be Done(TBD) one.
#  
#
# (C) 2021 Dawid Mudry, Tychy, Poland
# Released under GNU Public License (GPL)
# -----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# import requests as req
# import bs4
# import pandas as pd
# from datetime import datetime as dt
# import matplotlib.pyplot as plt
# from datetime import timedelta
# from datetime import date
# import time

class SimulatorEngine():
    def __init__(self, path, cash):
        self.path = path
        self.__data = self.__read_csv()[::-1]
        print(self.__data.keys())
        self.cash = cash


    def __read_csv(self):
        df = pd.read_csv(self.path)
        df.closeV = pd.to_numeric(df.closeV)
        return df


    def calculate_sma(self, windows):
        self.__data['MA'+str(windows)] = self.__data['closeV'].rolling(window=windows).mean()
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
        self.__data.plot(x='data', y=cv, kind = 'line', marker = '.')
        plt.show()
        return True


    def strategy(self):
        pos = 0
        num = 0
        self.percent_change = list()

        print(self.__data)

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