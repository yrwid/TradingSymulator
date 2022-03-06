from app.CsvDataController import CsvDataController
import pytest
import os
import tempfile

def test_erase_file():
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp, open('goldFiles/cdproject.csv', 'r') as goldenFile:
            for line in goldenFile:
                tmp.write(line)
        csv_controller = CsvDataController(path)
        csv_controller.erase()
        assert os.path.getsize(path) == 0
    finally:
        os.remove(path)
