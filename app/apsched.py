from aiogram import Bot
from aiogram.types import Message
from app.database.requests import get_reminders


# async def send_message_middleware(chat_id: int, bot: Bot):
#      reminders = await get_reminders(chat_id)
#      for reminder in reminders:

