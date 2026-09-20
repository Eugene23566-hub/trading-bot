import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AGENT_LOG_TOKEN = os.getenv("AGENT_LOG_TOKEN", "")


def send_log_to_agent(message):
    if not AGENT_LOG_TOKEN:
        return
    try:
        url = "https://trading-bot-0ffyba.fly.dev/log"
        headers = {"Authorization": AGENT_LOG_TOKEN, "Content-Type": "application/json"}
        payload = {"log": message}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Не удалось отправить лог:", response.status_code)
    except Exception as e:
        print("Ошибка при отправке лога:", e)


if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is not configured")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    log_msg = f"▶️ Команда /start от {message.from_user.full_name} (id: {message.from_user.id})"
    send_log_to_agent(log_msg)
    await message.answer("Привет! Бот работает ✅")


@dp.message()
async def echo_all(message: types.Message):
    log_msg = f"💬 Сообщение от {message.from_user.full_name}: {message.text}"
    send_log_to_agent(log_msg)
    await message.answer(f"Ты написал: {message.text}")


async def main():
    send_log_to_agent("🔄 Бот запущен и ожидает сообщения...")
    print("Бот запущен, ждёт сообщения…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
