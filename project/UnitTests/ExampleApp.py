from app.CsvDataController import CsvDataController
from app.DataManagerImpl import DataManagerImpl
from app.EngineImpl import EngineImpl
from app.GpwCollector import GpwCollector
from datetime import datetime as dt
from datetime import timedelta

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

    gpw_collector = GpwCollector()
    gpw_collector.set_instrument("CDPROJEKT")
    end = (dt.strptime(data_manager.read_last_record_date(), '%Y-%m-%d') + timedelta(days=10)).strftime('%Y-%m-%d')
    data_10days = gpw_collector.collect(start=data_manager.read_last_record_date(), stop=end)
    print("Gathered data from", data_manager.read_last_record_date(), "till", end, " : \n", data_10days)
    print("Time to refresh before appending:", data_manager.get_period_to_refresh())
    data_manager.append_df(data_10days)
    print("Time to refresh after appending:", data_manager.get_period_to_refresh())
