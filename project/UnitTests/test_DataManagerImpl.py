from app.DataManagerImpl import DataManagerImpl
from app import DataManagerImplExceptions as DataManagerExceptions
from app import CsvDataControllerExceptions as DataControllerExceptions
from datetime import datetime
import pytest
import pandas as pd

@pytest.fixture
def data_source_with_two_registered_sources():
    source_path_1 = "goldFiles/cdproject.csv"
    source_path_2 = "goldFiles/otherDataSource.csv"
    source_type_csv = "csv"
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", source_path_1, source_type_csv)
    data_manager.register_data_source("otherDataSource", source_path_2, source_type_csv)
    return data_manager


@pytest.fixture
def data_source_with_one_registered_sources():
    source_path_1 = "goldFiles/cdproject.csv"
    source_type_csv = "csv"
    data_manager = DataManagerImpl()
    data_manager.register_data_source("cdproject", source_path_1, source_type_csv)
    return data_manager


def test_register_correct_data_source():
    source_path = "goldFiles/cdproject.csv"
    source_type = "csv"
    data_manager = DataManagerImpl()
    try:
        data_manager.register_data_source("cdproject", source_path, source_type)
    except Exception as e:
        print(e)
        assert False


def test_register_incorrect_data_source():
    source_path = "goldFiles/abcdfg"
    source_type = "csv"
    data_manager = DataManagerImpl()
    with pytest.raises(DataControllerExceptions.WrongPathToFile):
        data_manager.register_data_source("cdproject", source_path, source_type)


def test_list_data_source(data_source_with_two_registered_sources):
    data_manager = data_source_with_two_registered_sources
    data_sources = data_manager.list_data_sources()
    data_sources_expected = [("cdproject", "csv"), ("otherDataSource", "csv")]
    assert data_sources == data_sources_expected


def test_get_current_data_source(data_source_with_two_registered_sources):
    data_manager = data_source_with_two_registered_sources
    current_data_source = data_manager.get_current_data_source_name()
    expected_data_source = ("cdproject", "csv")
    assert current_data_source == expected_data_source


def test_change_data_source(data_source_with_two_registered_sources):
    data_manager = data_source_with_two_registered_sources
    data_manager.change_data_source("otherDataSource")
    current_data_source = data_manager.get_current_data_source_name()
    expected_data_source = ("otherDataSource", "csv")
    assert current_data_source == expected_data_source


def test_read_last_record_date(data_source_with_one_registered_sources):
    data_manager = data_source_with_one_registered_sources
    data_manager_date = data_manager.read_last_record_date()
    expected_date = datetime(2021, 9, 8).strftime('%Y-%m-%d')
    assert expected_date == data_manager_date


def test_get_period_to_refresh(data_source_with_one_registered_sources):
    data_manager = data_source_with_one_registered_sources
    last_data_refresh_date = datetime(2021, 9, 8)
    now = datetime.today()
    delta = now - last_data_refresh_date

    data_manager_period = data_manager.get_period_to_refresh()
    assert data_manager_period == delta.days


def test_get_df(data_source_with_one_registered_sources):
    data_manager = data_source_with_one_registered_sources
    data_manager_df = data_manager.get_df()
    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    assert data_manager_df.equals(gold_file_data)


def test_call_without_registered_data_source():
    data_manager = DataManagerImpl()

    with pytest.raises(DataManagerExceptions.UnknownDataSourceName):
        data_manager.change_data_source("cdproject")

    with pytest.raises(DataManagerExceptions.DataSourceNotRegistered):
        data_manager.get_current_data_source_name()

    with pytest.raises(DataManagerExceptions.DataSourceNotRegistered):
        data_manager.list_data_sources()

    with pytest.raises(DataManagerExceptions.DataSourceNotRegistered):
        data_manager.get_df()

    with pytest.raises(DataManagerExceptions.DataSourceNotRegistered):
        data_manager.get_period_to_refresh()

    with pytest.raises(DataManagerExceptions.DataSourceNotRegistered):
        data_manager.read_last_record_date()

    df_obj = pd.DataFrame(columns=['User_ID', 'UserName', 'Action'])
    with pytest.raises(DataManagerExceptions.DataSourceNotRegistered):
        data_manager.append_df(df_obj)

    with pytest.raises(DataManagerExceptions.DataSourceNotRegistered):
        data_manager.overwrite_df(df_obj)


def test_unknown_format_type():
    source_name = "cdproject"
    source_path = "goldFiles/cdproject.csv"
    source_type = "lkm"
    data_manager = DataManagerImpl()
    with pytest.raises(DataManagerExceptions.UnknownDataTypeFormat):
        data_manager.register_data_source(source_name, source_path, source_type)


def test_unknown_data_source_name(data_source_with_one_registered_sources):
    unknown_data_source_name = "NotDataSourceName"
    data_manager = data_source_with_one_registered_sources
    with pytest.raises(DataManagerExceptions.UnknownDataSourceName):
        data_manager.change_data_source(unknown_data_source_name)
