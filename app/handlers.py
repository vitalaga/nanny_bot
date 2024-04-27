from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile, FSInputFile, URLInputFile
from aiogram.utils.markdown import hide_link
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.keyboards as kb
import app.database.requests as rq


router = Router()


class Reminder(StatesGroup):
    date_time = State()
    text = State()


@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>",
        reply_markup=kb.main,
        parse_mode='HTML')


@router.message(Command('set_reminder'))
async def set_reminder(message: Message, state: FSMContext):
    await state.set_state(Reminder.text)
    await message.answer("Введите текст напоминания")


@router.message(Reminder.text)
async def reminder_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Reminder.date_time)
    await message.answer('Введите дату и время напоминания в формате "ГГГГ-ММ-ДД ЧЧ:ММ" (например, 2023-12-31 23:59):')


@router.message(Reminder.date_time)
async def reminder_date(message: Message, state: FSMContext):
    try:
        date_time = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        await state.update_data(date_time=date_time)
        data = await state.get_data()
        await rq.set_reminder(message.from_user.id, data['date_time'], data['text'])
        await message.answer(
            f"Уведомление успешно добавлено\n"
            f"Текст напоминания: {data['text']}\n"
            f"Дата и время напоминания: {data['date_time']}\n"
        )
        await state.clear()

    except ValueError:
        await message.answer("Неверный формат даты и времени. Попробуйте снова.")


@router.callback_query(F.data == 'reminders')
async def reminders(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Вот все ваши напоминания:",
                                  reply_markup=await kb.reminders(callback.from_user.id)
                                  )


@router.callback_query(F.data.startswith('reminder_'))
async def reminder(callback: CallbackQuery):
    reminder_data = await rq.get_reminder(callback.data.split('_')[1])
    print(reminder_data)
    await callback.answer('Вы выбрали напоминание:')
    await callback.message.answer(f"Текст: {reminder_data.text}\n"
                                  f"Дата и время напоминания: {reminder_data.date_time}",
                                  reply_markup=await kb.reminders(callback.from_user.id)
                                  )


@router.message()
async def any_message(message: Message):
    text = message.text
    if text in ['Привет', 'привет', 'hi', 'hello']:
        await message.answer(f"И тебе привет {message.from_user.first_name}")
    else:
        await message.reply(
            f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
            f"Ничего не понятно, но очень интересно!", parse_mode='HTML')
