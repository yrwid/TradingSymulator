import requests as req
import bs4
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta


def liveCDRstocks():
    #Live price stocks 
    stocksCDP = 'PLOPTTC00011' 
    resp = req.get('https://www.gpw.pl/spolka?isin='+ stocksCDP)
    soup = bs4.BeautifulSoup(resp.text, "xml")
    livePrice =  soup.find_all('div',{'class' : 'max_min'})[0].find('span').text

    return livePrice.split()

def archStocks(instrument, data):
    try:
        resp = req.get('https://www.gpw.pl/archiwum-notowan-full?type=10&instrument='+instrument+'&date='+data)
        soup = bs4.BeautifulSoup(resp.text, "xml")
        temp = soup.find_all('table',{'class' : 'table footable'})[0].find_all('tr')[1].text.replace(",",".").replace(" ","")
        archStats = [string for string in list(map(lambda x: x.strip(), temp.split("\n"))) if string]
    except IndexError as e:
        print("Exeption occured")
        archStats = [instrument,data,'no data','no data','no data','no data','no data','no data','no data','no data','no data','no data']

    return archStats

def collectData(dataStart, dataEnd, instrument):
    start = dt.strptime(dataStart, '%d-%m-%Y')
    stop = dt.strptime(dataEnd, '%d-%m-%Y')
    delta = timedelta(days=1) 
    df = pd.DataFrame([])
    tmp = list()

    while start < stop:
        print("Downloading {} data... ".format(start.date()))
        stats = archStocks(instrument,start.strftime('%d-%m-%Y'))
        tmp.append(stats)
        start = start + delta # increase day one by one
        print("Done.")
        
    df = pd.DataFrame(tmp,columns=['Name','data','ISIN','currency','openV','maxV','minV','closeV','valueChagPer','vol','amountOfDeals','valueOfDeals'])
    col = ['openV','maxV','minV','closeV','valueChagPer','vol','amountOfDeals','valueOfDeals']
    df[col] = df[col].astype(float,errors = 'ignore')
    return df

def main():
    instrument = 'CDPROJEKT'
    # instrument2 = '11BIT'
    dataStart = '05-06-2020'
    dataEnd = '7-06-2020'
    print(collectData(dataStart,dataEnd,instrument))
    
if __name__ == '__main__':
    main()
    # s = '12,22'
    # s = float(s)
