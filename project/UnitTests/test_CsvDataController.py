from app.CsvDataController import CsvDataController
import pytest
import os
import tempfile
import pandas as pd

def test_erase_file():
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp, open('goldFiles/cdproject.csv', 'r') as goldenFile:
        for line in goldenFile:
            tmp.write(line)

    try:
        csv_controller = CsvDataController(path)
        csv_controller.erase()
        assert os.path.getsize(path) == 0
    finally:
        os.remove(path)


def test_append_file():
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp, open('goldFiles/cdproject.csv', 'r') as goldenFile:
        for line in goldenFile:
            tmp.write(line)

    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    try:
        csv_controller = CsvDataController(path)
        csv_controller.append(gold_file_data.iloc[-1])
        appended_file = pd.read_csv(path)
        first_line_in_file = appended_file.iloc[0]
        line_appended = gold_file_data.iloc[-1]

        # Start appending from top, not bottom.
        assert first_line_in_file == line_appended
    finally:
        os.remove(path)


def test_read_file():
    csv_controller = CsvDataController('goldFiles/cdproject.csv')
    df = csv_controller.read()
    gold_file_data = pd.read_csv('goldFiles/cdproject.csv')
    assert df.equals(gold_file_data)

def test_expections():
    assert False