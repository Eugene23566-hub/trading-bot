# signal_sources/trader_signals.py

import random

def get_trader_signal(symbol):
    # Пока что — заглушка, позже можно добавить парсинг TradingView
    return random.choice(["buy", "sell", "neutral"])
