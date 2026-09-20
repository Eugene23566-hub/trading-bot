from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
class Store:
    def __init__(self,path,starting_equity):
        Path(path).parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(path); self.db.row_factory=sqlite3.Row; self._init(starting_equity)
    def _init(self,starting_equity):
        c=self.db.cursor(); c.executescript("""
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS positions(id INTEGER PRIMARY KEY AUTOINCREMENT,symbol TEXT NOT NULL,side TEXT NOT NULL,entry REAL NOT NULL,stop REAL NOT NULL,target REAL NOT NULL,notional REAL NOT NULL,risk_usdt REAL NOT NULL,qty REAL NOT NULL,opened_at TEXT NOT NULL,closed_at TEXT,exit_price REAL,pnl_usdt REAL,r_multiple REAL,thesis TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'OPEN');
CREATE TABLE IF NOT EXISTS cycles(id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT NOT NULL,payload TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS setups(id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT NOT NULL,symbol TEXT NOT NULL,action TEXT NOT NULL,confidence REAL NOT NULL,rationale TEXT NOT NULL,payload TEXT NOT NULL);
"""); c.execute("INSERT OR IGNORE INTO meta(key,value) VALUES('equity',?)",(str(starting_equity),)); self.db.commit()
    def equity(self): return float(self.db.execute("SELECT value FROM meta WHERE key='equity'").fetchone()[0])
    def set_equity(self,e): self.db.execute("UPDATE meta SET value=? WHERE key='equity'",(str(e),)); self.db.commit()
    def open_positions(self): return list(self.db.execute("SELECT * FROM positions WHERE status='OPEN' ORDER BY id"))
    def total_open_notional(self): return float(self.db.execute("SELECT COALESCE(SUM(notional),0) FROM positions WHERE status='OPEN'").fetchone()[0])
    def add_position(self,p):
        cur=self.db.execute("INSERT INTO positions(symbol,side,entry,stop,target,notional,risk_usdt,qty,opened_at,thesis,status) VALUES(?,?,?,?,?,?,?,?,?,?, 'OPEN')",(p["symbol"],p["side"],p["entry"],p["stop"],p["target"],p["notional"],p["risk_usdt"],p["qty"],p["opened_at"],p["thesis"])); self.db.commit(); return int(cur.lastrowid)
    def close_position(self,pid,exit_price,pnl,r):
        ts=datetime.now(timezone.utc).isoformat(); self.db.execute("UPDATE positions SET status='CLOSED',closed_at=?,exit_price=?,pnl_usdt=?,r_multiple=? WHERE id=?",(ts,exit_price,pnl,r,pid)); self.set_equity(self.equity()+pnl)
    def add_setup(self,symbol,action,confidence,rationale,payload):
        self.db.execute("INSERT INTO setups(ts,symbol,action,confidence,rationale,payload) VALUES(?,?,?,?,?,?)",(datetime.now(timezone.utc).isoformat(),symbol,action,confidence,rationale,json.dumps(payload,ensure_ascii=False))); self.db.commit()
    def add_cycle(self,payload):
        self.db.execute("INSERT INTO cycles(ts,payload) VALUES(?,?)",(datetime.now(timezone.utc).isoformat(),json.dumps(payload,ensure_ascii=False))); self.db.commit()
