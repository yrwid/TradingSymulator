from abc import ABC, abstractmethod

# comment 1: if we first think about tests we can spot additional interfaces and dependencies.

class DataManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read_last_record_date(self):
        pass

    @abstractmethod
    def get_period_to_refresh(self):
        pass

    @abstractmethod
    def get_df(self):
        pass

    @abstractmethod
    def append_df(self, df):
        pass

    @abstractmethod
    def overwrite_df(self, df):
        pass

    @abstractmethod
    def register_data_source(self, path_to_source, source_type):
        pass

    @abstractmethod
    def list_data_sources(self):
        pass

    @abstractmethod
    def change_data_source(self, data_source_name):
        pass

    @abstractmethod
    def get_current_data_source(self):
        pass
