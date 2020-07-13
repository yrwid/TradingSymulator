import requests as req
import bs4
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import date

class GPW:
    def __init__(self, instrument,CDR):
        self.instrument = instrument
        self.CDR = CDR

    def liveCDRstocks(self):
        #Live price stocks 

        resp = req.get('https://www.gpw.pl/spolka?isin='+ self.CDR)
        soup = bs4.BeautifulSoup(resp.text, "xml")
        livePrice =  soup.find_all('div',{'class' : 'max_min'})[0].find('span').text

        return livePrice.split()

    def liveSpy(self):
        while True:
            print(self.liveCDRstocks())


    def archStocks(self,instrument, data):
        try:
            resp = req.get('https://www.gpw.pl/archiwum-notowan-full?type=10&instrument='+instrument+'&date='+data)
            soup = bs4.BeautifulSoup(resp.text, "xml")
            temp = soup.find_all('table',{'class' : 'table footable'})[0].find_all('tr')[1].text.replace(",",".").replace(" ","")
            archStats = [string for string in list(map(lambda x: x.strip(), temp.split("\n"))) if string]
        except IndexError as e:
            print("Exeption occured")
            archStats = [instrument,data,'no data','no data','no data','no data','no data','no data','no data','no data','no data','no data']

        return archStats

    def updateCsv(self, path):
        with open(path, "r") as f1:
            last_line = f1.readlines()[-1]
        
        tempDict = tuple(item for item in last_line.split(","))
        updateDates = list([tempDict[1], str(date.today().strftime('%d-%m-%Y') )])
        print(updateDates)


    def collectData(self, dataStart, dataEnd):
        start = dt.strptime(dataStart, '%d-%m-%Y')
        stop = dt.strptime(dataEnd, '%d-%m-%Y')
        delta = timedelta(days=1) 
        df = pd.DataFrame([])
        tmp = list()

        while start < stop:
            print("Downloading {} data... ".format(start.date()))
            stats = self.archStocks(self.instrument,start.strftime('%d-%m-%Y'))
            tmp.append(stats)
            start = start + delta # increase day one by one
            print("Done.")
            
        df = pd.DataFrame(tmp,columns=['Name','data','ISIN','currency','openV','maxV','minV','closeV','valueChagPer','vol','amountOfDeals','valueOfDeals'])
        col = ['openV','maxV','minV','closeV','valueChagPer','vol','amountOfDeals','valueOfDeals']
        df[col] = df[col].astype(float,errors = 'ignore')
        return df

def readCsv(path):
    cdp_df = pd.read_csv(path, header=0)
    # print(cdp_df)
    for i in range(len(cdp_df)):
        if(cdp_df.iloc[i,2] == 'no data' and i != 0 ):
            cdp_df.iloc[i,[2,3,7]] = cdp_df.iloc[i-1,[2,3,7]]
        elif(i == 0):
            for j in range(10):
                if(cdp_df.iloc[j,2] != 'no data'):
                    cdp_df.iloc[0,[2,3,7]] = cdp_df.iloc[j,[2,3,4]]
                    break
    # print(cdp_df)
    cdp_df.closeV = pd.to_numeric(cdp_df.closeV)
    cdp_df.to_csv('cdp_loaded.csv', index = False)
    return cdp_df

    

def rollingAvg(data, win):
    data['MA'+str(win)] = data['closeV'].rolling(window=win).mean()
    return data

def calculateEma(data, emasUsed):
    for x in emasUsed:
        ema = x
        data['EMA'+str(ema)] = round(data['closeV'].ewm(span=ema, adjust=False).mean(),2)
    return data

def makePlot(data, emasUsed):
    _y=['closeV']
    for ema in emasUsed:
        _y.append('EMA'+str(ema))
    data.plot(x ='data', y=_y, kind = 'line',marker = '.')
    plt.show()

def calculateSignals(data, emasUsed):
    pos = 0
    num = 0
    gains=0
    ng=0
    losses=0
    nl=0
    totalR=1

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

    print(percentChange)

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
    dataStart = '01-01-2020'
    dataEnd = '04-07-2020'
    instr = 'CDPROJEKT'
    CDR = 'PLOPTTC00011' 
    emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]
    
    cdproj = GPW(instr,CDR)
    cdproj.updateCsv('cdp_loaded.csv')
    # df = cdproj.collectData(dataStart,dataEnd)
    # cdproj.liveSpy()
    # df.to_csv('cdp.csv', index = False)
    # cdp_df = readCsv('cdp.csv')
    # cdp_df=calculateEma(cdp_df, emasUsed)
    # calculateSignals(cdp_df, emasUsed)
    # print(cdp_df.iloc[10,12:24])
    # makePlot(cdp_df,emasUsed)

if __name__ == '__main__':
    main()
