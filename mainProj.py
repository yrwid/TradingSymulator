import requests as req
import bs4
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from datetime import timedelta

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
    for i in range(len(cdp_df)):
        if(cdp_df.iloc[i,2] == 'no data'):
            cdp_df.iloc[i,[2,3,7]] = cdp_df.iloc[i-1,[2,3,7]]
    cdp_df.closeV = pd.to_numeric(cdp_df.closeV)
    return cdp_df

def main():
    dataStart = '01-06-2020'
    dataEnd = '30-06-2020'
    instr = 'CDPROJEKT'
    CDR = 'PLOPTTC00011' 
    # cdproj = GPW(instr,CDR)
    # df = cdproj.collectData(dataStart,dataEnd)
    # cdproj.liveSpy()
    # df.to_csv('cdp.csv', index = False)
    cdp_df = readCsv('cdp.csv')
    cdp_df.plot(x ='data', y='closeV', kind = 'line')
    # print(cdp_df)
    plt.show()

if __name__ == '__main__':
    main()
