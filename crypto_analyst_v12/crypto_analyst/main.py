from __future__ import annotations
import json, logging
from datetime import datetime, timezone
from .analyst import AIAnalyst
from .config import Settings
from .market import BinancePublic, Candidate, deep_features, fast_scan
from .notify import telegram
from .paper import derive_order, exit_from_candle, pnl_for
from .sheets import sync_setup, sync_trade
from .storage import Store
log=logging.getLogger("crypto-analyst")
def _market_context(features):
    by={f["symbol"]:f for f in features}; ctx={}
    for sym in ("BTCUSDT","ETHUSDT"):
        if sym in by:
            f=by[sym]; ctx[sym]={"price":f["price"],"trend_15m":f["trend_15m"],"trend_1h":f["trend_1h"],"rsi_15m":f["rsi_15m"],"rsi_1h":f["rsi_1h"],"change_24h_pct":f["change_24h_pct"]}
    return ctx
def run_cycle():
    cfg=Settings(); cfg.ensure_dirs()
    logging.basicConfig(level=getattr(logging,cfg.log_level.upper(),logging.INFO),format="%(asctime)s %(levelname)s %(message)s")
    api=BinancePublic(); store=Store(cfg.state_db,cfg.starting_equity); events=[]
    for p in store.open_positions():
        candle=api.klines(p["symbol"],"15m",2)[-1]; ex=exit_from_candle(p,candle)
        if ex:
            exit_price,reason=ex; pnl,r=pnl_for(p,exit_price); store.close_position(p["id"],exit_price,pnl,r)
            events.append({"type":"CLOSE","id":p["id"],"symbol":p["symbol"],"side":p["side"],"exit":exit_price,"pnl":pnl,"r":r,"reason":reason})
            sync_trade(cfg.google_service_account_file,cfg.google_sheet_id,[p["id"],p["opened_at"],datetime.now(timezone.utc).isoformat(),p["symbol"],p["side"],"v1.2 external",p["entry"],p["stop"],p["target"],p["notional"],p["risk_usdt"],exit_price,pnl,r,"Closed","","","","",p["thesis"],reason,"Binance public API"])
            telegram(cfg.telegram_bot_token,cfg.telegram_chat_id,f"Paper CLOSE {p['symbol']} {p['side']} | PnL {pnl:.2f} USDT | {r:.2f}R | {reason}")
    fast=fast_scan(api,cfg.max_candidates); symbols=[c.symbol for c in fast]
    for core in ("BTCUSDT","ETHUSDT"):
        if core not in symbols: fast.append(Candidate(core,0,0,0,0,0))
    deep=[]
    for c in fast[:max(cfg.deep_candidates,10)]:
        try: deep.append(deep_features(api,c))
        except Exception as exc: log.warning("deep features failed for %s: %s",c.symbol,exc)
    present={d["symbol"] for d in deep}
    for c in fast:
        if c.symbol in ("BTCUSDT","ETHUSDT") and c.symbol not in present:
            try: deep.append(deep_features(api,c))
            except Exception: pass
    context=_market_context(deep); candidates=[d for d in deep if d["symbol"] not in ("BTCUSDT","ETHUSDT")][:cfg.deep_candidates]
    if not cfg.openai_api_key:
        decisions={"market_regime":"mixed","decisions":[{"symbol":d["symbol"],"action":"WAIT","confidence":0.0,"setup_type":"AI_DISABLED","rationale":"OPENAI_API_KEY is not configured","risk_note":"No paper entry"} for d in candidates]}
    else: decisions=AIAnalyst(cfg.openai_api_key,cfg.openai_model).analyze(context,candidates)
    by={d["symbol"]:d for d in candidates}
    for d in decisions["decisions"]:
        if d["symbol"] not in by: continue
        store.add_setup(d["symbol"],d["action"],d["confidence"],d["rationale"],d)
        sync_setup(cfg.google_service_account_file,cfg.google_sheet_id,["",datetime.now(timezone.utc).isoformat(),d["symbol"],d["action"],"15m/1h",d["setup_type"],"market","ATR/structure","~2R",d["confidence"],"Watching" if d["action"]!="WAIT" else "Rejected",d["rationale"],"","",d["risk_note"],"Binance + OpenAI"])
    actionable=sorted([d for d in decisions["decisions"] if d["action"] in ("LONG","SHORT") and d["confidence"]>=cfg.min_ai_confidence],key=lambda x:x["confidence"],reverse=True)
    if actionable and len(store.open_positions())<cfg.max_open_positions:
        best=actionable[0]; f=by[best["symbol"]]; equity=store.equity(); remaining=max(0,equity*cfg.max_total_notional_multiple-store.total_open_notional()); order=derive_order(f,best["action"],equity,cfg.risk_per_trade,remaining)
        if order:
            order["thesis"]=best["rationale"]; pid=store.add_position(order); events.append({"type":"OPEN","id":pid,**order,"confidence":best["confidence"],"setup_type":best["setup_type"]})
            sync_trade(cfg.google_service_account_file,cfg.google_sheet_id,[pid,order["opened_at"],"",order["symbol"],order["side"],best["setup_type"],order["entry"],order["stop"],order["target"],order["notional"],order["risk_usdt"],"","","","Open","","",decisions["market_regime"],order["thesis"],"","Binance + OpenAI"])
            telegram(cfg.telegram_bot_token,cfg.telegram_chat_id,f"Paper OPEN {order['symbol']} {order['side']} @ {order['entry']:.8g} | SL {order['stop']:.8g} | TP {order['target']:.8g} | risk {order['risk_usdt']:.2f} USDT")
    result={"ts":datetime.now(timezone.utc).isoformat(),"equity":store.equity(),"market_regime":decisions["market_regime"],"events":events,"decisions":decisions["decisions"]}; store.add_cycle(result); log.info("cycle complete: %s",json.dumps(result,ensure_ascii=False)); return result
if __name__=="__main__": run_cycle()
