import asyncio
import os
import logging

from aiogram import Bot, Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.handlers import router
from app.database.models import async_main
from app.database.requests import check_notification

from middlewares.apschedulermiddleware import SchedulerMiddleware

from dotenv import load_dotenv


load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    await async_main()

    dp.include_router(router)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(check_notification, trigger='interval', seconds=60, kwargs={'bot': bot})
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
