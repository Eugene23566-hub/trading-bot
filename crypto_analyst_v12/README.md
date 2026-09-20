# Crypto Analyst v1.2 — 15-minute paper-trading agent
External scanner for the Crypto Analyst project.

## Safety boundary
- Paper trading only.
- No Binance order endpoint exists in this module.
- Binance API keys are not required.
- Default risk: 0.5% equity per paper trade.
- Max 3 open paper positions.
- Total notional <= 1x equity.
- Ambiguous stop/target candle => stop first.

## Flow
Binance public data -> fast scan (50) -> deep features (10) -> OpenAI structured decision -> deterministic risk engine -> SQLite -> optional Google Sheets + Telegram.

## Install on Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y git python3 python3-venv rsync
git clone https://github.com/Eugene23566-hub/trading-bot.git
cd trading-bot/crypto_analyst_v12
sudo ./deploy/install.sh
sudo nano /opt/crypto-analyst/.env
sudo systemctl start crypto-analyst.timer
sudo systemctl start crypto-analyst.service
systemctl list-timers | grep crypto-analyst
journalctl -u crypto-analyst.service -n 100 --no-pager
```

## Required secret
`OPENAI_API_KEY`

Optional: Telegram token/chat id and Google service-account JSON.

Google Trade Journal ID:
`1sA0J3Q43E9AgBU8QRgxS_6-5P4OeKya91hLIrmTPLZ0`

For Google Sheets sync, share the sheet with the service-account email and place its JSON at:
`/opt/crypto-analyst/secrets/google-service-account.json`

SQLite is canonical for the external 15-minute loop. Google Sheets is the reporting mirror.
