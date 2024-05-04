from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def actions_reminders(reminder_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_reminder_{reminder_id}"),
         ]
    ])
    return keyboard
