from app.DataController import *
from app.CsvDataControllerExceptions import *
import pandas as pd
import os.path


class CsvDataController(DataController):
    def __init__(self, path):
        if os.path.isfile(path):
            self.path = path
        else:
            raise WrongPathToFile

    def erase(self):
        # Opening and closing with only w flag will erase file.
        open(self.path, 'w').close()

    def append(self, data_frame):
        data_frame.to_csv(self.path, mode='a', index=False, header=False)

    def read(self):
        try:
            df = pd.read_csv(self.path)
        except:
            raise UnabledToReadFromFileToDataFrame
        return df
