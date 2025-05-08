# strategies/rsi_ema_strategy.py

from strategies.base_strategy import BaseStrategy

class RsiEmaStrategy(BaseStrategy):
    def should_enter(self, indicators, news_sentiment, trader_signal):
        return (
            indicators['rsi'] < 35 and
            news_sentiment != "bearish" and
            trader_signal != "sell"
        )
