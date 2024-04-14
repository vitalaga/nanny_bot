from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile, FSInputFile, URLInputFile
from aiogram.utils.markdown import hide_link
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from datetime import datetime

import app.keyboards as kb
import app.database.requests as rq


router = Router()


class Reminder(StatesGroup):
    text = State()
    date = State()
    time = State()


@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>", reply_markup=kb.main, parse_mode='HTML')


@router.message(Command("show_list"))
async def cmd_show_list(message: Message, mylist: list[int]):
    await message.answer(f"Ваш список: {mylist}")


@router.message(Command("add_to_list"))
async def cmd_add_to_list(message: Message, mylist: list[int]):
    try:
        value = message.text.split(" ")
        mylist.append(int(value[1]))
        await message.answer(f"Добавлено число {value[1]}")
    except ValueError:
        await message.answer("Ошибочное значение! Пожалуйста, введите число в формате '/add_to_list число'")
    except IndexError:
        await message.answer("Ошибочное значение! Пожалуйста, введите число в формате '/add_to_list число'")


@router.callback_query(F.data == 'how_are_you')
async def how_are_you(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('OK!😁😁😁😁')


@router.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)


# @router.message(Command('images'))
# async def upload_photo(message: Message):
#     """Хэндлер для отправки фото(тест)"""
#     file_ids = []
#     with open("buffer_emulation.jpg", "rb") as image_from_buffer:
#         result = await message.answer_photo(
#             BufferedInputFile(
#                 image_from_buffer.read(),
#                 filename="image from buffer.jpg"
#             ),
#             caption="Изображение из буфера"
#         )
#         file_ids.append(result.photo[-1].file_id)
#
#     image_from_pc = FSInputFile("image_from_pc.jpg")
#     result = await message.answer_photo(
#         image_from_pc,
#         caption="Изображение из файла на компьютере"
#     )
#     file_ids.append(result.photo[-1].file_id)
#
#     image_from_url = URLInputFile(
#         "https://android-obzor.com/wp-content/uploads/2022/05/ss_a6885ca2f2d6a87715238754157727b553e7884b.1920x1080.jpg"
#     )
#     result = await message.answer_photo(
#         image_from_url,
#         caption="Изображение по ссылке"
#     )
#     file_ids.append(result.photo[-1].file_id)
#     await message.answer("Отправленные файлы: \n" + "\n".join(file_ids))


@router.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"D:/{message.photo[-1].file_id}.jpg"
    )


# @router.message(F.sticker)
# async def download_stocker(message: Message, bot: Bot):
#     await bot.download(
#         message.sticker,
#         destination=f"D:/{message.sticker.file_id}.webp"
#     )


@router.message(F.audio)
async def download_sound(message: Message, bot: Bot):
    await bot.download(
        message.audio,
        destination=f"D:/{message.audio.file_name}"
    )


@router.message(Command('reminder'))
async def reminder(message: Message, state: FSMContext):
    await state.set_state(Reminder.text)
    await message.answer("Введите текст напоминания")


@router.message(Reminder.text)
async def reminder_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Reminder.date)
    await message.answer("Введите дату напоминания в формате ДД.ММ.ГГГГ")


@router.message(Reminder.date)
async def reminder_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(Reminder.time)
    await message.answer("Введите время напоминания в формате ЧЧ:ММ")


@router.message(Reminder.time)
async def reminder_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()
    await rq.set_reminder(text=data['text'], date=data['date'], time=data['time'], tg_id=message.from_user.id)
    await message.answer(
        f"Текст напоминания: {data['text']}\n"
        f"Дата напоминания: {data['date']}\n"
        f"Время напоминания: {data['time']}"
    )
    await state.clear()





@router.message()
async def any_message(message: Message):
    text = message.text
    if text in ['Привет', 'привет', 'hi', 'hello']:
        await message.answer(f"И тебе привет {message.from_user.first_name}")
    else:
        await message.reply(
            f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
            f"Ничего не понятно, но очень интересно!", parse_mode='HTML')
