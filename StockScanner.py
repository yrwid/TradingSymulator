# -----------------------------------------------------------
# Class for scanning poland stocks.
#
# Keep in mind this class is To Be Done(TBD) one.
#  
#
# (C) 2021 Dawid Mudry, Tychy, Poland
# Released under GNU Public License (GPL)
# -----------------------------------------------------------

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