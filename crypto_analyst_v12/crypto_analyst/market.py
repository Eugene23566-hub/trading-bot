from __future__ import annotations
import time, requests
from dataclasses import dataclass
from .indicators import atr, ema, macd, rsi, volume_ratio
SPOT="https://api.binance.com"; FUTURES="https://fapi.binance.com"
EXCLUDED_BASES={"USDC","FDUSD","TUSD","USDP","DAI","EUR","TRY","BRL","UP","DOWN","BULL","BEAR"}
@dataclass
class Candidate:
    symbol:str; last_price:float; quote_volume:float; change_24h:float; range_24h:float; score:float
class BinancePublic:
    def __init__(self,timeout=10.0): self.s=requests.Session(); self.timeout=timeout
    def _get(self,base,path,params=None):
        last=None
        for attempt in range(3):
            try:
                r=self.s.get(base+path,params=params,timeout=self.timeout); r.raise_for_status(); return r.json()
            except requests.RequestException as exc:
                last=exc; time.sleep(0.5*(attempt+1))
        raise RuntimeError(f"Binance request failed: {path}: {last}")
    def tickers_24h(self): return self._get(SPOT,"/api/v3/ticker/24hr")
    def klines(self,symbol,interval,limit=120): return self._get(SPOT,"/api/v3/klines",{"symbol":symbol,"interval":interval,"limit":limit})
    def funding(self,symbol):
        try: return float(self._get(FUTURES,"/fapi/v1/premiumIndex",{"symbol":symbol})["lastFundingRate"])
        except Exception: return None
    def open_interest(self,symbol):
        try: return float(self._get(FUTURES,"/fapi/v1/openInterest",{"symbol":symbol})["openInterest"])
        except Exception: return None
def _tradable_usdt(symbol):
    if not symbol.endswith("USDT"): return False
    base=symbol[:-4]
    return base not in EXCLUDED_BASES and not base.endswith(("UP","DOWN","BULL","BEAR"))
def fast_scan(api,max_candidates=50):
    out=[]
    for t in api.tickers_24h():
        s=t.get("symbol","")
        if not _tradable_usdt(s): continue
        try:
            q=float(t["quoteVolume"]); last=float(t["lastPrice"]); ch=float(t["priceChangePercent"]); hi=float(t["highPrice"]); lo=float(t["lowPrice"])
        except Exception: continue
        if q<5_000_000 or last<=0: continue
        rng=(hi-lo)/last*100 if last else 0
        score=min(q/50_000_000,10)+min(abs(ch)/3,5)+min(rng/3,5)
        out.append(Candidate(s,last,q,ch,rng,score))
    out.sort(key=lambda c:(c.score,c.quote_volume),reverse=True); return out[:max_candidates]
def _series(k):
    return [float(x[2]) for x in k],[float(x[3]) for x in k],[float(x[4]) for x in k],[float(x[5]) for x in k]
def deep_features(api,c):
    k15=api.klines(c.symbol,"15m",120); k1h=api.klines(c.symbol,"1h",120)
    h15,l15,c15,v15=_series(k15); h1,l1,c1,v1=_series(k1h)
    e20_15,e50_15=ema(c15,20)[-1],ema(c15,50)[-1]; e20_1,e50_1=ema(c1,20)[-1],ema(c1,50)[-1]
    *_,mh15=macd(c15); *_,mh1=macd(c1); a15=atr(h15,l15,c15,14)
    return {"symbol":c.symbol,"price":c15[-1],"change_24h_pct":c.change_24h,"quote_volume_24h":c.quote_volume,"range_24h_pct":c.range_24h,
    "rsi_15m":rsi(c15),"rsi_1h":rsi(c1),"ema20_15m":e20_15,"ema50_15m":e50_15,"ema20_1h":e20_1,"ema50_1h":e50_1,
    "macd_hist_15m":mh15,"macd_hist_1h":mh1,"atr_15m":a15,"atr_pct_15m":a15/c15[-1]*100 if a15 else None,
    "volume_ratio_15m":volume_ratio(v15),"recent_low_3h":min(l15[-12:]),"recent_high_3h":max(h15[-12:]),
    "funding_rate":api.funding(c.symbol),"open_interest":api.open_interest(c.symbol),
    "trend_15m":"up" if e20_15>e50_15 else "down","trend_1h":"up" if e20_1>e50_1 else "down"}
