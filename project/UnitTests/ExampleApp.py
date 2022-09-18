from app.CsvDataController import CsvDataController
from app.DataManagerImpl import DataManagerImpl
from app.EngineImpl import EngineImpl
from app.GpwCollector import GpwCollector
from datetime import datetime as dt
from datetime import timedelta
from test_EngineImpl import StrategyBasedOnEmaData
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

if __name__ == "__main__":
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdprojekt", "goldFiles/cdprojekt_full.csv", "csv")
    print("Current data source name and type:",data_manager.get_current_data_source_name())
    print("Data hasn't been refreshed since:", data_manager.read_last_record_date())
    print("Time to refresh till today:", data_manager.get_period_to_refresh())

    data_manager.register_data_source("cdprojekt_copy", "goldFiles/cdprojekt_full_copy.csv", "csv")
    print("Data source name after appeding another data source:", data_manager.get_current_data_source_name())
    data_manager.change_data_source("cdprojekt_copy")
    print("Data source name after changing data source", data_manager.get_current_data_source_name())
    print("Data sources list:", data_manager.list_data_sources())

    # gpw_collector = GpwCollector()
    # gpw_collector.set_instrument("CDPROJEKT")
    # end = (dt.strptime(data_manager.read_last_record_date(), '%Y-%m-%d') + timedelta(days=10)).strftime('%Y-%m-%d')
    # data_10days = gpw_collector.collect(start=data_manager.read_last_record_date(), stop=end)
    # print("Gathered data from", data_manager.read_last_record_date(), "till", end, " : \n", data_10days)
    # print("Time to refresh before appending:", data_manager.get_period_to_refresh())
    # data_manager.append_df(data_10days)
    # print("Time to refresh after appending:", data_manager.get_period_to_refresh())

    df = data_manager.get_df()
    eng = EngineImpl(df)
    ema_based_test_strategy = StrategyBasedOnEmaData(stocks_bought_already=False)
    eng.set_strategy(ema_based_test_strategy)
    buy_sell_signals = eng.run(dt(2010, 1, 4))
    bss = buy_sell_signals
    # 8, 10, 12, 15, 20, 30, 35, 40, 45, 50, 60

    # make figure + axes
    fig, ax = plt.subplots(tight_layout=True)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    # helper function for the formatter
    def listifed_formatter(x, pos=None):
        try:
            return bss["date"][int(x)]
        except IndexError:
            return ''

    # draw one line
    ax.plot(bss["price"], lw=4)
    ax.plot(bss["emas"]["5"], lw=2)
    ax.plot(bss["emas"]["8"], lw=2)
    ax.plot(bss["emas"]["10"], lw=2)
    ax.plot(bss["emas"]["12"], lw=2)
    ax.plot(bss["emas"]["15"], lw=2)
    ax.plot(bss["emas"]["20"], lw=2)
    ax.plot(bss["emas"]["30"], lw=2)
    ax.plot(bss["emas"]["35"], lw=2)
    ax.plot(bss["emas"]["40"], lw=2)
    ax.plot(bss["emas"]["45"], lw=2)
    ax.plot(bss["emas"]["50"], lw=2)
    ax.plot(bss["emas"]["60"], lw=2)

    # make and use the formatter
    mt = mticker.FuncFormatter(listifed_formatter)
    ax.xaxis.set_major_formatter(mt)

    # set the default ticker to only put ticks on the integers
    loc = ax.xaxis.get_major_locator()
    loc.set_params(integer=True)

    # rotate the labels
    [lab.set_rotation(30) for lab in ax.get_xticklabels()]

 #    plt.plot(bss["price"], bss["price"])
 #    plt.plot(bss["price"], bss["emas"]["5"])
 #    plt.xticks(len(bss["date"]), bss["date"])
 # #             bss["emas"]["5"],
 # #             bss["emas"]["8"],
 # #             bss["emas"]["10"],
 # #             bss["emas"]["12"],
 # #             bss["emas"]["15"],
 # #             bss["emas"]["20"],
 # #             bss["emas"]["30"],
 # #             bss["emas"]["35"],
 # #             bss["emas"]["40"],
 # #             bss["emas"]["45"],
 # #             bss["emas"]["50"],
 # #             bss["emas"]["60"])

    plt.show()
    # plt.savefig('plot.png', dpi=1200)

    # cv=['closeV']
    # for ema in self.emas_used:
    #     cv.append('EMA'+str(ema))
    # self.__data.plot(x='data', y=cv, kind = 'line', marker = '.')
    # plt.show()



