from sqlalchemy import BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Reminder(Base):
    __tablename__ = 'reminders'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    date_time: Mapped[str] = mapped_column(DateTime)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))


