from app.GpwCollector import GpwCollector
import pandas as pd

# time logged: 3h, 1,5h

def test_compare_collected_data_to_golden_file():
    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    start = '2021-09-08'
    end = '2021-08-27'
    collected_data = GpwCollector().collect(start, end)
    assert gold_file_data.equals(collected_data)


# def test_improper_date():
#     collected_data = GpwCollector().collect()
#     assert gold_file_data.equals(collected_data)