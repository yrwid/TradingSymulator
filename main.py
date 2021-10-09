# -----------------------------------------------------------
# Example uses of project.
#
# Keep in mind this class is To Be Done(TBD) one.
#  
#
# (C) 2021 Dawid Mudry, Tychy, Poland
# Released under GNU Public License (GPL)
# -----------------------------------------------------------

# TO DO:
# Finish stocks scanner class.  
# Add docstrings to methods. 
# Implement abstract class  in strategy class. 
# Implement green line breakout.
# Do something with indicators (more reusable code).  
# Expand abstract class.
# Create IBD Realative strength indicator. 
# Better plots (more reusable code).
# Check imports if really necessary.
# Add needed python module requirment to requirments.txt.lock

# local imports
from gpwCollector import GpwDataLoader as gpwDL

def main():
    date_start = '04-01-2013'
    date_end = '26-09-2021'
    instr = 'CDPROJEKT'
    i_start = 26# 26 sie wysypało sprawdzic to 
    # i_stop =  27
    # emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]

    collector = gpwDL(instr, date_start, date_end)
    collector.update_csv("cdprojekt.csv");
    # collector.flipCsvFile("cdprojekt.csv");
    # collector.read_gpw_stock(instr)
    # collector.update_csv(instr + ".csv")
    # df  = gpwdt.__collect_data(date_start, date_end, 'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=')
    # gpwdt.save_csv('WIG.csv', df, 'stock' )
    # print(gpwdt.save_csv.__doc__)
    # gpwdt.update_all_csv()
    # eng = SimulatorEngine('cdprojekt.csv', 10000)
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
