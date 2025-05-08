# ema.py

import pandas as pd
from pandas_ta.utils import get_offset, verify_series

def ema(close, length=None, offset=None, **kwargs):
    """Exponential Moving Average (EMA)"""
    length = int(length) if length and length > 0 else 10
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    ema = close.ewm(span=length, min_periods=length).mean()

    # Offset
    if offset != 0:
        ema = ema.shift(offset)

    # Name & Category
    ema.name = f"EMA_{length}"
    ema.category = "trend"

    return ema
