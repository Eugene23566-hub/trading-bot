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
    await message.answer("Привет! Бот работает ✅")

# Обработка всех текстовых сообщений
@dp.message()
async def echo_all(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# Основной цикл
async def main():
    print("Бот запущен, ждёт сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
