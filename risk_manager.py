# risk_manager.py

import datetime

DAILY_LIMIT = {
    "max_profit_pct": 10,   # % от стартового депозита
    "max_loss_pct": 5,
    "max_trades": 10
}

trade_log = []
start_balance = 1000  # фиксированная точка отсчёта

def can_trade(balance, predicted_prob=None):
    now = datetime.datetime.utcnow().date()
    trades_today = [t for t in trade_log if t["date"] == str(now)]

    profit_today = sum(t["profit"] for t in trades_today)
    profit_pct = 100 * profit_today / start_balance

    # Исключение: если модель предсказывает >80% успеха — разрешить
    if predicted_prob and predicted_prob > 0.8:
        return True, "🧠 Вероятность успеха > 80% — торговля разрешена"

    if len(trades_today) >= DAILY_LIMIT["max_trades"]:
        return False, "🔴 Превышено количество сделок за день"
    if profit_pct >= DAILY_LIMIT["max_profit_pct"]:
        return False, "🟢 Достигнута дневная цель по прибыли"
    if profit_pct <= -DAILY_LIMIT["max_loss_pct"]:
        return False, "🔴 Превышен лимит убытков"
    
    return True, "✅ Торговля разрешена"

def log_trade(profit):
    trade_log.append({
        "date": str(datetime.datetime.utcnow().date()),
        "profit": profit
    })
