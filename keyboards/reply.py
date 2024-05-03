from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
     [KeyboardButton(text='Создать напоминание',)],
     [KeyboardButton(text='Активные напоминания',),
      KeyboardButton(text='Контакты')],
 ],
 )





