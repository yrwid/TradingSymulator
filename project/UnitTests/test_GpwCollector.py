from app.GpwCollector import GpwCollector
import pandas as pd
import pytest
from app import GpwCollectorExceptions as gpwe


# time logged: 3h, 1,5h, 1h

def test_compare_collected_data_to_golden_file():
    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    start = '2021-08-27'
    end = '2021-09-08'
    collected_data = GpwCollector().collect(start, end)
    assert gold_file_data.equals(collected_data)


def test_same_start_end_dates():
    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    start = '2021-09-08'
    end = '2021-09-08'
    collected_data = GpwCollector().collect(start, end)
    assert collected_data.equals(gold_file_data.iloc[0])


def test_improper_start_date():
    end = '2022-01-01'

    random_start_date = 'asdfgrgdsa'
    with pytest.raises(gpwe.WrongStartDate):
        GpwCollector().collect(random_start_date, end)

    ancient_start_date = '1650-01-22'
    with pytest.raises(gpwe.WrongStartDate):
        GpwCollector().collect(ancient_start_date, end)

    wrong_format_date_month_first = '09-2021-08'
    with pytest.raises(gpwe.WrongStartDate):
        GpwCollector().collect(wrong_format_date_month_first, end)

    wrong_format_date_day_first = '29-08-2021'
    with pytest.raises(gpwe.WrongStartDate):
        GpwCollector().collect(wrong_format_date_day_first, end)

    wrong_format_date_too_much_days = '2021-08-60'
    with pytest.raises(gpwe.WrongStartDate):
        GpwCollector().collect(wrong_format_date_too_much_days, end)

    wrong_format_date_too_much_months = '2021-60-08'
    with pytest.raises(gpwe.WrongStartDate):
        GpwCollector().collect(wrong_format_date_too_much_months, end)


def test_improper_end_date():
    start = '2021-09-08'

    random_end_date = 'axdfgxgdsx'
    with pytest.raises(gpwe.WrongStartDate):
        GpwCollector().collect(start, random_end_date)

    end_date_before_start_date = '2021-01-01'
    with pytest.raises(gpwe.WrongEndDate):
        GpwCollector().collect(start, end_date_before_start_date)

    end_date_ancient = '1650-01-22'
    with pytest.raises(gpwe.WrongEndDate):
        GpwCollector().collect(start, end_date_ancient)

    wrong_format_date_month_first = '09-2021-08'
    with pytest.raises(gpwe.WrongEndDate):
        GpwCollector().collect(start, wrong_format_date_month_first)

    wrong_format_date_day_first = '29-08-2021'
    with pytest.raises(gpwe.WrongEndDate):
        GpwCollector().collect(start, wrong_format_date_day_first)

    wrong_format_date_too_much_days = '2021-08-60'
    with pytest.raises(gpwe.WrongEndDate):
        GpwCollector().collect(start, wrong_format_date_too_much_days)

    wrong_format_date_too_much_months = '2021-60-08'
    with pytest.raises(gpwe.WrongEndDate):
        GpwCollector().collect(start, wrong_format_date_too_much_months)

