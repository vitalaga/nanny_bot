from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_reminders, get_reminder


main = ReplyKeyboardMarkup(keyboard=[
     [KeyboardButton(text='Создать напоминание',)],
     [KeyboardButton(text='Активные напоминания',),
      KeyboardButton(text='Контакты')],
 ],
 )


async def reminders(tg_id):
    all_reminders = await get_reminders(tg_id)
    keyboard = InlineKeyboardBuilder()
    for reminder in all_reminders:
        keyboard.add(InlineKeyboardButton(text=reminder.text, callback_data=f"reminder_{reminder.id}"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data='start'))
    return keyboard.adjust(2).as_markup()


# async def reminder(tg_id, reminder_id):
#     all_reminders = await get_reminders(tg_id)
#     keyboard = InlineKeyboardBuilder()
#     for reminder in all_reminders:
#         keyboard.add(InlineKeyboardButton(text=reminder.text, callback_data=f"reminder_{reminder.id}"))
#     keyboard.add(InlineKeyboardButton(text="На главную", callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()




