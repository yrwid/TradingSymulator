from app.DataManager import DataManager
from app.CsvDataController import CsvDataController
from app.DataManagerImplExceptions import *
from app.CsvDataControllerExceptions import *
from datetime import datetime


class DataManagerImpl(DataManager):
    def __init__(self):
        self.data_sources = list()
        self.data_source_indicator = 0

    def read_last_record_date(self):
        df = self.get_df()
        return df["Date"].iloc[-1]

    def get_period_to_refresh(self):
        last_date = self.read_last_record_date()
        return (datetime.now() - datetime.strptime(last_date, '%Y-%m-%d')).days

    def get_df(self):
        data_source = self.__get_current_data_source_handle()
        return data_source.read()

    def append_df(self, df):
        data_source = self.__get_current_data_source_handle()
        data_source.append(df)

    def overwrite_df(self, df):
        data_source = self.__get_current_data_source_handle()
        data_source.erase()
        data_source.append(df)

    def register_data_source(self, data_source_name, path_to_source, source_type):
        data_source_handle = self.__create_low_level_data_controller(path_to_source, source_type)
        self.data_sources.append({"name" : data_source_name,
                                  "type" : source_type,
                                  "handle" : data_source_handle})

    def list_data_sources(self):
        self.__thrown_exception_if_no_data_source_is_available()
        current_data_sources = list()

        for data_source in self.data_sources:
            current_data_sources.append(tuple([data_source["name"], data_source["type"]]))
        return current_data_sources

    def change_data_source(self, data_source_name_to_find):
        for index, data_source in enumerate(self.data_sources):
            if data_source["name"] == data_source_name_to_find:
                self.data_source_indicator = index
                return
        raise UnknownDataSourceName

    def get_current_data_source_name(self):
        current_data_source = self.__get_current_data_source()
        return tuple([current_data_source["name"], current_data_source["type"]])

    @staticmethod
    def __create_low_level_data_controller(path_to_source, source_type):
        if source_type == "csv":
            data_controller = CsvDataController(path_to_source)
        else:
            raise UnknownDataTypeFormat
        return data_controller

    def __get_current_data_source(self):
        self.__thrown_exception_if_no_data_source_is_available()
        return self.data_sources[self.data_source_indicator]

    def __get_current_data_source_handle(self):
        self.__thrown_exception_if_no_data_source_is_available()
        return self.data_sources[self.data_source_indicator]["handle"]

    def __thrown_exception_if_no_data_source_is_available(self):
        if len(self.data_sources) is 0:
            raise DataSourceNotRegistered
