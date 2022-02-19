from app.GpwCollector import GpwCollector
import pandas as pd
import pytest
from app import GpwCollectorExceptions as gpwe


# time logged: 3h, 1,5h, 1h, || 1h, 1h

# Comment 1: With easy interface there is easier to write tests,
# more arguments in interface makes tests harder to write,
# therefore we are focusing more on good defined interfaces at the beginning.

# Comment 2: You can spot needed interface during test writing, before actual implementation.

# Comment 3: Helps identify various errors or new exceptions.

@pytest.fixture()
def set_up():
    gpw_collector = GpwCollector()
    gpw_collector.set_instrument("CDPROJEKT")
    return gpw_collector


def test_unknown_stock_name():
    gpw_collector = GpwCollector()
    start = '2021-08-27'
    end = '2021-09-08'
    with pytest.raises(gpwe.StockNameNotExist):
        gpw_collector.collect(start, end)


def test_compare_collected_data_to_golden_file(set_up):
    gpw_collector = set_up
    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    start = '2021-08-27'
    end = '2021-09-08'
    collected_data = gpw_collector.collect(start, end)
    assert gold_file_data.equals(collected_data)


def test_same_start_end_dates(set_up):
    gpw_collector = set_up
    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    start = '2021-09-08'
    end = '2021-09-08'
    collected_data = gpw_collector.collect(start, end)
    golden_file_day_one = gold_file_data.iloc[[0]]
    assert collected_data.equals(golden_file_day_one)


def test_random_start_date(set_up):
    gpw_collector = set_up
    end = '2022-01-01'

    random_start_date = 'asdfgrgdsa'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(random_start_date, end)


def test_ancient_start_date(set_up):
    gpw_collector = set_up
    end = '2022-01-01'

    ancient_start_date = '1650-01-22'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(ancient_start_date, end)


def test_wrong_format_date_month_first_start_date(set_up):
    gpw_collector = set_up
    end = '2022-01-01'

    wrong_format_date_month_first = '09-2021-08'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(wrong_format_date_month_first, end)


def test_wrong_format_date_day_first_start_date(set_up):
    gpw_collector = set_up
    end = '2022-01-01'

    wrong_format_date_day_first = '29-08-2021'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(wrong_format_date_day_first, end)


def test_wrong_format_date_too_much_days_start_date(set_up):
    gpw_collector = set_up
    end = '2022-01-01'

    wrong_format_date_too_much_days = '2021-08-60'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(wrong_format_date_too_much_days, end)


def test_wrong_format_date_too_much_months_start_date(set_up):
    gpw_collector = set_up
    end = '2022-01-01'

    wrong_format_date_too_much_months = '2021-60-08'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(wrong_format_date_too_much_months, end)


def test_random_end_date(set_up):
    gpw_collector = set_up
    start = '2021-09-08'

    random_end_date = 'axdfgxgdsx'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(start, random_end_date)


def test_end_date_before_start_date(set_up):
    gpw_collector = set_up
    start = '2021-09-08'

    end_date_before_start_date = '2021-01-01'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(start, end_date_before_start_date)


def test_end_date_ancient(set_up):
    gpw_collector = set_up
    start = '2021-09-08'

    end_date_ancient = '1650-01-22'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(start, end_date_ancient)


def test_wrong_format_date_month_first_end_date(set_up):
    gpw_collector = set_up
    start = '2021-09-08'

    wrong_format_date_month_first = '09-2021-08'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(start, wrong_format_date_month_first)


def test_wrong_format_date_day_first_end_date(set_up):
    gpw_collector = set_up
    start = '2021-09-08'

    wrong_format_date_day_first = '29-08-2021'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(start, wrong_format_date_day_first)


def test_wrong_format_date_too_much_days_end_date(set_up):
    gpw_collector = set_up
    start = '2021-09-08'

    wrong_format_date_too_much_days = '2021-08-60'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(start, wrong_format_date_too_much_days)


def test_wrong_format_date_too_much_months_end_date(set_up):
    gpw_collector = set_up
    start = '2021-09-08'

    wrong_format_date_too_much_months = '2021-60-08'
    with pytest.raises(gpwe.WrongInputDate):
        gpw_collector.collect(start, wrong_format_date_too_much_months)

