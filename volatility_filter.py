# volatility_filter.py

from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

def get_top_volatile_symbols(limit=5, interval='1h'):
    tickers = client.get_ticker()
    symbols = []

    for t in tickers:
        if t['symbol'].endswith('USDT') and not any(x in t['symbol'] for x in ['UP', 'DOWN', 'BULL', 'BEAR']):
            try:
                change = abs(float(t['priceChangePercent']))
                symbols.append((t['symbol'], change))
            except:
                continue

    top = sorted(symbols, key=lambda x: x[1], reverse=True)[:limit]
    return [s[0] for s in top]
