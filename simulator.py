# simulator.py

def simulate_trade(symbol, side, quantity, price, balance):
    total = round(price * quantity, 2)
    trade = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "price": price,
        "total": total
    }

    if side == "BUY":
        if balance.get("USDT", 0) >= total:
            balance["USDT"] -= total
            balance[symbol] = balance.get(symbol, 0) + quantity
        else:
            print("❌ Недостаточно USDT для покупки")
    elif side == "SELL":
        if balance.get(symbol, 0) >= quantity:
            balance[symbol] -= quantity
            balance["USDT"] += total
        else:
            print("❌ Недостаточно актива для продажи")
    else:
        print("❌ Неверный тип сделки")

    return trade, balance
