from app.database.models import async_session
from app.database.models import User, Reminder

from sqlalchemy import select, update, delete

from datetime import datetime


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_reminder(tg_id, date_time, text):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return None
        else:
            session.add(Reminder(user=user.id, date_time=date_time, text=text))
            await session.commit()


async def check_notification(bot):
    async with (async_session() as session):
        while True:

            notifications = await session.scalars(select(Reminder).where(Reminder.date_time <= datetime.now()))

            for notification in notifications:
                user = await session.scalar(select(User).where(User.id == notification.user))
                tg_id = user.tg_id
                text = notification.text

                await bot.send_message(tg_id, text)

                await session.delete(notification)
                await session.commit()



