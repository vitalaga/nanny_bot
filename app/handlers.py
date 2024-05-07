from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hide_link
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from datetime import datetime

import keyboards.reply as kb_reply
import keyboards.inline as kb_inline
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
        reply_markup=kb_reply.main,
        parse_mode='HTML')


@router.message(F.text == 'Создать напоминание')
async def set_reminder(message: Message, state: FSMContext):
    await state.set_state(Reminder.text)
    await message.answer("Введите текст напоминания:")


@router.message(Reminder.text)
async def reminder_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Reminder.date_time)
    await message.answer('Введите дату в формате ДД.ММ.ГГГГ и время в формате ЧЧ:ММ (например, 31.12.2023 23:59):')


@router.message(Reminder.date_time)
async def reminder_date(message: Message, state: FSMContext):
    try:
        date_time = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        await state.update_data(date_time=date_time)
        data = await state.get_data()
        await rq.set_reminder(message.from_user.id, data['date_time'], data['text'])

        await message.answer(
            f"Уведомление успешно добавлено\n"
            f"<b>Текст напоминания:</b> {data['text']}\n"
            f"<b>Дата и время напоминания:</b> {date_time.strftime('%d.%m.%Y в %H:%M')}\n",
            parse_mode='HTML'
        )
        await state.clear()

    except ValueError:
        await message.answer("Неверный формат даты и времени. Попробуйте снова.")


@router.message(F.text.lower() == 'Активные напоминания'.lower())
async def all_reminders(message: Message):
    reminders_user = rq.get_reminders(message.from_user.id)
    if reminders_user:
        await message.answer("<strong>Вот все ваши напоминания:</strong>", parse_mode='HTML')
        for rem in await reminders_user:
            await message.answer(f"<b>Текст:</b> {rem.text}\n<b>Дата и время напоминания:</b> {rem.date_time}",
                                 parse_mode='HTML',
                                 reply_markup=await kb_inline.actions_reminders(rem.id)
                                 )
    else:
        await message.answer("Активных напоминаний нет😢")


@router.callback_query(F.data.startswith('delete_reminder_'))
async def delete_reminder(callback: CallbackQuery):
    reminder_data = await rq.get_reminder(callback.data.split('_')[-1])
    await callback.answer(
        f'Вы удалили напоминание {reminder_data.text}'
        f'\n на {reminder_data.date_time}',
        show_alert=True)
    await rq.delete_reminder(callback.data.split('_')[-1])


@router.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"D:/{message.photo[-1].file_id}.jpg"
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
