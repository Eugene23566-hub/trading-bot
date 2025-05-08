name = "pandas_ta"
"""
.. moduleauthor:: Kevin Johnson
"""

__version__ = "0.3.14b-local"

from importlib.util import find_spec

Imports = {
    "alphaVantage-api": find_spec("alphaVantageAPI") is not None,
    "matplotlib": find_spec("matplotlib") is not None,
    "mplfinance": find_spec("mplfinance") is not None,
    "scipy": find_spec("scipy") is not None,
    "sklearn": find_spec("sklearn") is not None,
    "statsmodels": find_spec("statsmodels") is not None,
    "stochastic": find_spec("stochastic") is not None,
    "talib": find_spec("talib") is not None,
    "tqdm": find_spec("tqdm") is not None,
    "vectorbt": find_spec("vectorbt") is not None,
    "yfinance": find_spec("yfinance") is not None,
}

Category = {
    "candles": ["cdl_doji", "cdl_inside", "ha"],
    "cycles": ["ebsw"],
    "momentum": [
        "ao", "apo", "bias", "bop", "brar", "cci", "cfo", "cg", "cmo",
        "coppock", "er", "eri", "fisher", "inertia", "kdj", "kst", "macd",
        "mom", "pgo", "ppo", "psl", "pvo", "qqe", "roc", "rsi", "rsx", "rvgi",
        "slope", "smi", "squeeze", "stoch", "stochrsi", "td_seq", "trix", "tsi", "uo",
        "willr"
    ],
    "overlap": [
        "alma", "dema", "ema", "fwma", "hilo", "hl2", "hlc3", "hma", "ichimoku",
        "kama", "linreg", "mcgd", "midpoint", "midprice", "ohlc4", "pwma", "rma",
        "sinwma", "sma", "ssf", "supertrend", "swma", "t3", "tema", "trima",
        "vidya", "vwap", "vwma", "wcp", "wma", "zlma"
    ],
    "performance": ["log_return", "percent_return", "trend_return"],
    "statistics": [
        "entropy", "kurtosis", "mad", "median", "quantile", "skew", "stdev",
        "variance", "zscore"
    ],
    "trend": [
        "adx", "amat", "aroon", "chop", "cksp", "decay", "decreasing", "dpo",
        "increasing", "long_run", "psar", "qstick", "short_run", "ttm_trend",
        "vortex"
    ],
    "volatility": [
        "aberration", "accbands", "atr", "bbands", "donchian", "hwc", "kc", "massi",
        "natr", "pdist", "rvi", "thermo", "true_range", "ui"
    ],
    "volume": [
        "ad", "adosc", "aobv", "cmf", "efi", "eom", "mfi", "nvi", "obv", "pvi",
        "pvol", "pvr", "pvt"
    ],
}

CANGLE_AGG = {
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
}

EXCHANGE_TZ = {
    "NZSX": 12, "ASX": 11, "TSE": 9, "HKE": 8, "SSE": 8, "SGX": 8,
    "NSE": 5.5, "DIFX": 4, "RTS": 3, "JSE": 2, "FWB": 1, "LSE": 1,
    "BMF": -2, "NYSE": -4, "TSX": -4
}

RATE = {
    "DAYS_PER_MONTH": 21,
    "MINUTES_PER_HOUR": 60,
    "MONTHS_PER_YEAR": 12,
    "QUARTERS_PER_YEAR": 4,
    "TRADING_DAYS_PER_YEAR": 252,
    "TRADING_HOURS_PER_DAY": 6.5,
    "WEEKS_PER_YEAR": 52,
    "YEARLY": 1,
}

from pandas_ta.core import *
