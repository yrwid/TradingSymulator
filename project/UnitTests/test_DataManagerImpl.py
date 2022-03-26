from app.DataManagerImpl import DataManagerImpl
# from app import CsvDataControllerExceptions as cdce
import pytest
import os
import tempfile
import pandas as pd

# TODO: add fixture

def test_register_correct_data_source():
    source_path = "goldFiles/cdproject"
    source_type = "csv"
    data_manager = DataManagerImpl()
    assert data_manager.register_data_source(source_path, source_type)


def test_register_incorrect_data_source():
    source_path = "goldFiles/abcdfg"
    source_type = "csv"
    data_manager = DataManagerImpl(source_path, source_type)
    assert not data_manager.register_data_source(source_path, source_type)


def test_list_data_source():
    source_path_1 = "goldFiles/cdproject"
    source_path_2 = "goldFiles/otherDataSource.csv"
    source_type_csv = "csv"

    data_manager = DataManagerImpl()
    data_manager.register_data_source(source_path_1, source_type_csv)
    data_manager.register_data_source(source_path_2, source_type_csv)
    data_sources = data_manager.list_data_sources()
    data_sources_expected = [("cdprojekt", "csv"), ("otherDataSource", "csv")]
    assert  data_sources == data_sources_expected


def test_get_current_data_source():
    source_path_1 = "goldFiles/cdproject"
    source_path_2 = "goldFiles/otherDataSource.csv"
    source_type_csv = "csv"

    data_manager = DataManagerImpl()
    data_manager.register_data_source(source_path_1, source_type_csv)
    data_manager.register_data_source(source_path_2, source_type_csv)
    current_data_source = data_manager.get_current_data_source()
    expected_data_source = ("otherDataSource", "csv")
    assert  current_data_source == expected_data_source


def test_change_data_source():
    source_path_1 = "goldFiles/cdproject"
    source_path_2 = "goldFiles/otherDataSource.csv"
    source_type_csv = "csv"

    data_manager = DataManagerImpl()
    data_manager.register_data_source(source_path_1, source_type_csv)
    data_manager.register_data_source(source_path_2, source_type_csv)
    data_manager.change_data_source("cdproject")
    current_data_source = data_manager.get_current_data_source()
    expected_data_source = ("cdproject", "csv")
    assert  current_data_source == expected_data_source


def test_read_last_record_date():
    pass


def test_get_period_to_refresh():
    pass


def test_get_df():
    pass


def test_append_df():
    pass


def test_overwrite_df():
    pass

