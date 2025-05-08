# strategies/base_strategy.py

class BaseStrategy:
    def should_enter(self, indicators, news_sentiment, trader_signal):
        raise NotImplementedError("Реализуй этот метод в дочернем классе")
