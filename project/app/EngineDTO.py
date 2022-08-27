from typing import NamedTuple
from datetime import datetime


class EngineDTO(NamedTuple):
    """ emaX - exponential moving average with window based on X days"""

    date: datetime
    currentClosePrice: float
    ema5: float
    ema8: float
    ema10: float
    ema12: float
    ema15: float
    ema20: float
    ema30: float
    ema35: float
    ema40: float
    ema45: float
    ema50: float
    ema60: float

