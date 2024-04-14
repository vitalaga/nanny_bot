import asyncio
import logging
from aiogram import Bot, Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import apsched

from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot("6741441734:AAGVkBYuRDRUewADSY46aOs1LRrV9pC-_Yw")
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    dp.include_router(router)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
