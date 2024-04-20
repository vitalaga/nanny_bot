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
