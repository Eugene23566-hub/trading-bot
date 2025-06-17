import requests

def send_log_to_agent(message):
    try:
        url = "https://trading-bot-0ffyba.fly.dev/log"
        headers = {"Authorization": "08111990", "Content-Type": "application/json"}
        payload = {"log": message}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print("Не удалось отправить лог:", response.text)
    except Exception as e:
        print("Ошибка при отправке лога:", e)

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
print(f"TOKEN: {TELEGRAM_TOKEN}")  # проверка

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    log_msg = f"▶️ Команда /start от {message.from_user.full_name} (id: {message.from_user.id})"
    send_log_to_agent(log_msg)
    await message.answer("Привет! Бот работает ✅")

# Обработка всех текстовых сообщений
@dp.message()
async def echo_all(message: types.Message):
    log_msg = f"💬 Сообщение от {message.from_user.full_name}: {message.text}"
    send_log_to_agent(log_msg)
    await message.answer(f"Ты написал: {message.text}")

# Основной цикл
async def main():
    send_log_to_agent("🔄 Бот запущен и ожидает сообщения...")
    print("Бот запущен, ждёт сообщения…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
