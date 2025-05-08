from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_current_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"[!] Ошибка получения цены {symbol}: {e}")
        return None

# binance_api.py

from binance.client import Client
import config

client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)


def get_current_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"[Ошибка Binance] Не удалось получить цену для {symbol}: {e}")
        return None
