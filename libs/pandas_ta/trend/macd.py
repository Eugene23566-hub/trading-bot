import pandas as pd
from pandas_ta.utils import get_offset, verify_series

def macd(close, fast=12, slow=26, signal=9, offset=0, **kwargs):
    """Moving Average Convergence Divergence (MACD)"""
    close = verify_series(close)
    offset = get_offset(offset)

    # Validate inputs
    if close is None or len(close) == 0:
        return None

    # Calculate MACD
    fast_ema = close.ewm(span=fast, min_periods=fast).mean()
    slow_ema = close.ewm(span=slow, min_periods=slow).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal, min_periods=signal).mean()
    histogram = macd - signal_line

    # Offset
    if offset != 0:
        macd = macd.shift(offset)
        signal_line = signal_line.shift(offset)
        histogram = histogram.shift(offset)

    # Naming
    macd.name = f"MACD_{fast}_{slow}_{signal}"
    signal_line.name = f"MACDs_{fast}_{slow}_{signal}"
    histogram.name = f"MACDh_{fast}_{slow}_{signal}"
    macd.category = signal_line.category = histogram.category = "trend"

    # Combine
    df = pd.concat([macd, signal_line, histogram], axis=1)
    return df
