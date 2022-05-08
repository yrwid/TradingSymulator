from typing import NamedTuple


class EngineDTO(NamedTuple):
    """ emaX - exponential moving average with window based on X days"""

    currentClosePrice: float
    ema5: float
    ema8: float
    ema10: float
    ema12: float
    ema15: float
    ema30: float
    ema35: float
    ema40: float
    ema45: float
    ema50: float
    ema60: float

