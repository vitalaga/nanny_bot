import asyncio
import os
import logging

from aiogram import Bot, Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.handlers import router
from app.database.engine import create_db
from app.database.requests import check_notification

from dotenv import load_dotenv


load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    await create_db()

    dp.include_router(router)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(check_notification, trigger='interval', seconds=60, misfire_grace_time=3, kwargs={'bot': bot})
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот отключён.')
