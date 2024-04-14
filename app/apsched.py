from aiogram import Bot
from aiogram.types import Message
from database.requests import get_remind


async def send_message_cron(message: Message, bot: Bot):
    await bot.send_message(get_remind(message.from_user.id))
