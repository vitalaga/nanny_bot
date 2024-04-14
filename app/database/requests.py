from app.database.models import async_session
from app.database.models import User, Reminder

from sqlalchemy import select, update, delete


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_reminder(text, date, time, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return None
        else:
            session.add(Reminder(text=text, date=date, time=time, user=user.id))
            await session.commit()


async def get_remind(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Reminder.text).where(User.tg_id == tg_id))
