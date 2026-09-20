from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
def _f(name: str, default: float) -> float: return float(os.getenv(name, str(default)))
def _i(name: str, default: int) -> int: return int(os.getenv(name, str(default)))
@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    starting_equity: float = _f("STARTING_EQUITY", 9950.0)
    risk_per_trade: float = _f("RISK_PER_TRADE", 0.005)
    max_open_positions: int = _i("MAX_OPEN_POSITIONS", 3)
    max_total_notional_multiple: float = _f("MAX_TOTAL_NOTIONAL_MULTIPLE", 1.0)
    min_ai_confidence: float = _f("MIN_AI_CONFIDENCE", 0.72)
    max_candidates: int = _i("MAX_CANDIDATES", 50)
    deep_candidates: int = _i("DEEP_CANDIDATES", 10)
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    google_service_account_file: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
    google_sheet_id: str = os.getenv("GOOGLE_SHEET_ID", "")
    state_db: str = os.getenv("STATE_DB", "./state/crypto_analyst.sqlite3")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    def ensure_dirs(self) -> None:
        Path(self.state_db).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
