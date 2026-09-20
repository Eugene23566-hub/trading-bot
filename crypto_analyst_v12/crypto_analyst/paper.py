from datetime import datetime, timezone
def derive_order(f,side,equity,risk_fraction,remaining_notional):
    price=float(f["price"]); a=f.get("atr_15m")
    if not a or a<=0 or price<=0: return None
    if side=="LONG":
        structural=float(f["recent_low_3h"]); stop=min(price-1.2*a,structural*0.998); rpu=price-stop; target=price+2*rpu
    else:
        structural=float(f["recent_high_3h"]); stop=max(price+1.2*a,structural*1.002); rpu=stop-price; target=price-2*rpu
    if rpu<=0: return None
    risk=equity*risk_fraction; qty=min(risk/rpu,max(0,remaining_notional)/price)
    if qty<=0: return None
    return {"symbol":f["symbol"],"side":side,"entry":price,"stop":stop,"target":target,"qty":qty,"notional":qty*price,"risk_usdt":qty*rpu,"opened_at":datetime.now(timezone.utc).isoformat()}
def exit_from_candle(p,c):
    hi=float(c[2]); lo=float(c[3]); stop=float(p["stop"]); target=float(p["target"])
    if p["side"]=="LONG": sh,th=lo<=stop,hi>=target
    else: sh,th=hi>=stop,lo<=target
    if sh and th: return stop,"STOP_AMBIGUOUS_FIRST"
    if sh: return stop,"STOP"
    if th: return target,"TARGET"
    return None
def pnl_for(p,exit_price):
    qty=float(p["qty"]); entry=float(p["entry"]); pnl=(exit_price-entry)*qty if p["side"]=="LONG" else (entry-exit_price)*qty; risk=float(p["risk_usdt"]); return pnl,pnl/risk if risk else 0
