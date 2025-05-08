# telegram_bot/bot.py

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
import json
import datetime
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

LOG_FILE = "data/trade_history.json"

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("🤖 Привет! Я торговый бот. Используй команды: /status, /profit, /log")

@dp.message_handler(commands=["status"])
async def status_handler(message: types.Message):
    await message.answer("📡 Бот работает. Анализирует рынок и симулирует сделки.")

@dp.message_handler(commands=["profit"])
async def profit_handler(message: types.Message):
    today = str(datetime.datetime.utcnow().date())
    try:
        with open(LOG_FILE, 'r') as f:
            trades = json.load(f)
        today_trades = [t for t in trades if t["date"] == today]
        profit = round(sum(t["profit"] for t in today_trades), 2)
        await message.answer(f"💰 Прибыль за сегодня: <b>{profit} USDT</b>")
    except:
        await message.answer("❌ Нет данных о сделках за сегодня.")

@dp.message_handler(commands=["log"])
async def log_handler(message: types.Message):
    try:
        with open(LOG_FILE, 'r') as f:
            trades = json.load(f)[-5:]
        text = "\n".join([f"{t['symbol']} {t['side']} по {t['price']} → {t['profit']} USDT" for t in trades])
        await message.answer(f"🧾 Последние сделки:\n{text}")
    except:
        await message.answer("❌ Логи недоступны.")
from aiogram import executor

def run_bot():
    executor.start_polling(dp, skip_updates=True)

