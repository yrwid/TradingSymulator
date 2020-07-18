import requests as req
import bs4
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import date
import time

class GPW_DataLoader:
    def __init__(self, instrument, dateStart,dateEnd):
        self.instrument = instrument
        self.dateStart = dateStart
        self.dateEnd = dateEnd

    def __archStocks(self,instrument, data):
        try:
            resp = req.get('https://www.gpw.pl/archiwum-notowan-full?type=10&instrument='+instrument+'&date='+data)
            soup = bs4.BeautifulSoup(resp.text, "xml")
            temp = soup.find_all('table',{'class' : 'table footable'})[0].find_all('tr')[1].text.replace(",",".").replace(" ","")
            archStats = [string for string in list(map(lambda x: x.strip(), temp.split("\n"))) if string]
        except IndexError as e:
            print("Exeption occured")
            archStats = [instrument,data,'no data','no data','no data','no data','no data','no data','no data','no data','no data','no data']

        return archStats

    def saveCSV(self,path, df):
        for i in range(len(df)):
            if(df.iloc[i,2] == 'no data' and i != 0 ):
                df.iloc[i,[2,3,7]] = df.iloc[i-1,[2,3,7]]
            elif(i == 0):
                for j in range(10):
                    if(df.iloc[j,2] != 'no data'):
                        df.iloc[0,[2,3,7]] = df.iloc[j,[2,3,4]]
                        break
        df.closeV = pd.to_numeric(df.closeV)
        df.to_csv(path, index = False) 

    def updateCsv(self, path):
        with open(path, "r") as f1:
            last_line = f1.readlines()[-1]
        
        tempDict = tuple(item for item in last_line.split(","))
        startDate = ((dt.strptime(tempDict[1], '%d-%m-%Y') + timedelta(days=1)).date()).strftime('%d-%m-%Y')
        updateDates = list([str(startDate) , str(date.today().strftime('%d-%m-%Y') )])
        df = self.collectData(updateDates[0],updateDates[1])

        for i in range(len(df)):
            if(df.iloc[i,2] == 'no data' and i != 0 ):
                df.iloc[i,[2,3,7]] = df.iloc[i-1,[2,3,7]]
            elif(i == 0):
                df.iloc[i,2] = tempDict[2] 
                df.iloc[i,3] = tempDict[3]
                df.iloc[i,7] = tempDict[7]
        df.to_csv(path, mode='a', header=False, index = False)

    def collectData(self, dateStart, dateEnd):
        start = dt.strptime(dateStart, '%d-%m-%Y')
        stop = dt.strptime(dateEnd, '%d-%m-%Y')
        delta = timedelta(days=1) 
        df = pd.DataFrame([])
        tmp = list()

        while start <= stop:
            print("Downloading {} data... ".format(start.date()))
            stats = self.__archStocks(self.instrument,start.strftime('%d-%m-%Y'))
            tmp.append(stats)
            start = start + delta # increase day one by one
            print("Done.")
            
        df = pd.DataFrame(tmp,columns=['Name','data','ISIN','currency','openV','maxV','minV','closeV','valueChagPer','vol','amountOfDeals','valueOfDeals'])
        col = ['openV','maxV','minV','closeV','valueChagPer','vol','amountOfDeals','valueOfDeals']
        df[col] = df[col].astype(float,errors = 'ignore')
        return df

    def readGpwStocks(self,dateStart,dateEnd,i_start, i_stop):
        excelGpwStocks = 'gpwStocks.xlsx'
        gpwStocks = pd.read_excel(excelGpwStocks, index_col=False)
        # print(gpwStocks)
        for i  in range(i_start,i_stop): #(len(gpwStocks))
            print('Now: {}'.format(str(gpwStocks.iloc[i,0])))
            companyName = gpwStocks.iloc[i,0]  # 11bit-studio ISIN
            self.instrument = companyName
            df = self.collectData(dateStart,dateEnd)
            self.saveCSV(str(gpwStocks.iloc[i,0]) + '.csv',df)

#--------------------------------------------------------------------------------------------------------------------------------------------

class simulatorEngine():
    def __init__(self, path, cash):
        self.path = path
        self.__data = self.__readCsv()
        self.cash = cash

    def __readCsv(self):
        df = pd.read_csv(self.path)
        df.closeV = pd.to_numeric(df.closeV)
        return df

    def calculateSMA(self,windows):
        self.__data['MA'+str(win)] = self.__data['closeV'].rolling(window=win).mean()
        return True

    def calculateEMA(self,emasUsed):
        self.emasUsed = emasUsed
        for x in emasUsed:
            ema = x
            self.__data['EMA'+str(ema)] = round(self.__data['closeV'].ewm(span=ema, adjust=False).mean(),2)
        return True

    def makePlot(self):
        _y=['closeV']
        for ema in self.emasUsed:
            _y.append('EMA'+str(ema))
        self.__data.plot(x ='data', y=_y, kind = 'line',marker = '.')
        plt.show()
        return True

    def strategyEMA(self,data, emasUsed):
        indktrs = {
                "pos" : 0,
                "num" : 0,
                "gains" : 0,
                "ng" : 0,
                "losses" : 0,
                "nl" : 0,
                "totalR" : 1,
                "percentChange" : list()
            }  

        pos = 0
        num = 0
        gains = 0
        ng = 0
        losses = 0
        nl = 0
        totalR = 1
        percentChange = list()

        for i in data.index:
            cmin = min(data['EMA5'][i],data['EMA8'][i],data['EMA10'][i],data['EMA12'][i],data['EMA15'][i])  
            cmax = max(data['EMA30'][i],data['EMA35'][i],data['EMA40'][i],data['EMA45'][i],data['EMA50'][i],data['EMA60'][i])
            close = data['closeV'][i] 

            if(cmin > cmax):
                if(pos == 0):
                    bp = close
                    pos = 1
                    print('Buying at {}, data:{} '.format(bp,data['data'][i]))

            elif(cmin < cmax):
                if(pos == 1):
                    sp = close
                    pos = 0
                    print('selling at {}, data:{} '.format(sp,data['data'][i]))
                    pc = (sp/bp - 1)*100
                    percentChange.append(pc)

            if(num == data['closeV'].count()-1 and pos == 1):
                pos = 0
                sp = close
                print('executing sell at end of data, price: {}, data:{}'.format(sp,data['data'][i]))
                pc = (sp/bp - 1)*100
                percentChange.append(pc)

            num+=1

        return True

    def indicators(self):

        for i in percentChange:
            if(i>0):
                gains+=i
                ng+=1
            else:
                losses+=i
                nl+=1
            totalR=totalR*((i/100)+1)

        totalR=round((totalR-1)*100,2)

        if(ng>0):
            avgGain=gains/ng
            maxR=str(max(percentChange))
        else:
            avgGain=0
            maxR="undefined"

        if(nl>0):
            avgLoss=losses/nl
            maxL=str(min(percentChange))
            ratio=str(-avgGain/avgLoss)
        else:
            avgLoss=0
            maxL="undefined"
            ratio="inf"

        if(ng>0 or nl>0):
            battingAvg=ng/(ng+nl)
        else:
            battingAvg=0

        print()
        print("Results for stocks going back to "+str(data['data'][0])+", Sample size: "+str(ng+nl)+" trades")
        print("EMAs used: "+str(emasUsed))
        print("Batting Avg: "+ str(battingAvg))
        print("Gain/loss ratio: "+ ratio)
        print("Average Gain: "+ str(avgGain))
        print("Average Loss: "+ str(avgLoss))
        print("Max Return: "+ maxR)
        print("Max Loss: "+ maxL)
        print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
        print()

def main():
    dateStart = '01-01-2020'
    dateEnd = '16-07-2020'
    instr = 'CDPROJEKT'
    i_start = 20 # 10 to 20 of gpw stocks 
    i_stop =  30
    emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]

    gpwdt = GPW_DataLoader(instr,dateStart,dateEnd)
    # eng = simulatorEngine('11BIT.csv')
    # eng.calculateEMA(emasUsed)
    # eng.makePlot()
    gpwdt.readGpwStocks(dateStart,dateEnd,i_start,i_stop)

if __name__ == '__main__':
    main()
