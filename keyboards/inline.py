from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_reminders, get_reminder


async def actions_reminders(reminder_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_reminder_{reminder_id}"),
         InlineKeyboardButton(text="Изменить", callback_data=f"update_reminder_{reminder_id}")]
    ])
    return keyboard


# async def reminder(tg_id, reminder_id):
#     all_reminders = await get_reminders(tg_id)
#     keyboard = InlineKeyboardBuilder()
#     for reminder in all_reminders:
#         keyboard.add(InlineKeyboardButton(text=reminder.text, callback_data=f"reminder_{reminder.id}"))
#     keyboard.add(InlineKeyboardButton(text="На главную", callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()