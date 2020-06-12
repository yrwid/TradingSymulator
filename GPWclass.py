import requests as req
import bs4
import pandas as pd

def liveCDRstocks():
    #Live price stocks 
    stocksCDP = 'PLOPTTC00011' 
    resp = req.get('https://www.gpw.pl/spolka?isin='+ stocksCDP)
    soup = bs4.BeautifulSoup(resp.text, "xml")
    livePrice =  soup.find_all('div',{'class' : 'max_min'})[0].find('span').text

    return livePrice.split()

def archStocks(instrument, data):
    resp = req.get('https://www.gpw.pl/archiwum-notowan-full?type=10&instrument='+instrument+'&date='+data)
    soup = bs4.BeautifulSoup(resp.text, "xml")
    temp = soup.find_all('table',{'class' : 'table footable'})[0].find_all('tr')[1].text
    archStats = [string for string in list(map(lambda x: x.strip(), temp.split("\n"))) if string]

    return archStats

def collectData(start, emd, instrument):
    tmp = list()
    stats = archStocks(instrument,start)
    tmp.append(stats)
    df = pd.DataFrame(tmp,columns=['Name','data','ISIN','currency','openV','maxV','minV','closeV','valueChagPer','vol','amountOfDeals','valueOfDeals'])
    return df

def main():
    instrument = 'CDPROJEKT'
    dataStart = '10-06-2020'
    dataEnd = '12-06-2020'
    print(collectData(dataStart,dataEnd,instrument))
    

if __name__ == '__main__':
    main()