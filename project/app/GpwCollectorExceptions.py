

class WrongStartDate(Exception):
    """Exception raised when start data is in bad format,
    too early i.e before 1970 or after current date"""

class WrongEndDate(Exception):
    """Exception raised when End data is in bad format,
    before start date, too early i.e before 1970 or after current date"""