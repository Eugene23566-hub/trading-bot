#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${1:-https://github.com/Eugene23566-hub/trading-bot.git}"
BRANCH="${2:-main}"
APP=/opt/crypto-analyst
if ! id cryptoanalyst >/dev/null 2>&1; then sudo useradd --system --home "$APP" --shell /usr/sbin/nologin cryptoanalyst; fi
sudo mkdir -p "$APP" "$APP/state" "$APP/secrets"
sudo chown -R "$USER":cryptoanalyst "$APP"
TMP=$(mktemp -d)
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TMP/repo"
rsync -a --delete --exclude '.env' "$TMP/repo/crypto_analyst_v12/" "$APP/"
python3 -m venv "$APP/.venv"
"$APP/.venv/bin/pip" install --upgrade pip
"$APP/.venv/bin/pip" install -r "$APP/requirements.txt"
if [[ ! -f "$APP/.env" ]]; then cp "$APP/.env.example" "$APP/.env"; chmod 600 "$APP/.env"; fi
sudo cp "$APP/deploy/crypto-analyst.service" /etc/systemd/system/
sudo cp "$APP/deploy/crypto-analyst.timer" /etc/systemd/system/
sudo chown -R cryptoanalyst:cryptoanalyst "$APP/state" "$APP/secrets"
sudo systemctl daemon-reload
sudo systemctl enable crypto-analyst.timer
echo "Edit $APP/.env, then start timer and run one manual cycle."
