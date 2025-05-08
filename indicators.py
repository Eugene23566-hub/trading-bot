import pandas as pd
import pandas_ta as ta
from binance.client import Client
from config import API_KEY, API_SECRET

client = Client(API_KEY, API_SECRET)

def get_klines(symbol, interval='5m', limit=100):
    raw = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(raw, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df

def compute_indicators(df):
    df.ta.rsi(length=14, append=True)                                # Добавит колонку RSI_14
    df.ta.ema(length=20, append=True)                                # Добавит колонку EMA_20
    df.ta.macd(fast=12, slow=26, signal=9, append=True)              # Добавит MACD_12_26_9, MACDs_12_26_9, MACDh_12_26_9
    return df
