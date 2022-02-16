

class WrongInputDate(Exception):
    """Exception raised when start, stop data is in bad format,
    too early i.e before 1970 or after current date"""

class StockNameNotExist(Exception):
    """Exception raised when stock name is wrong or legacy"""
