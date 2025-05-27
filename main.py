import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from studentbid import user_private_router
from hasardier_SQL import init_db
from utils import schedule_jobs

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    raise ValueError("Не удалось загрузить переменные из .env")

logger.add("bot.log", rotation="10 MB", level="INFO")
logger.info("Бот запущен")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(user_private_router)

async def on_startup():
    await init_db()
    asyncio.create_task(schedule_jobs(bot))

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())