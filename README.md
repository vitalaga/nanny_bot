![image](https://i.ibb.co/vVVgzcH/photo-2024-02-06-23-40-41-fotor-20240513193931.jpg)
# **Nanny Bot**
[![Supported Python versions](https://img.shields.io/pypi/pyversions/python-telegram-bot-raw.svg)](https://pypi.org/project/python-telegram-bot-raw/)

___
Этот репозиторий содержит Telegram-бота, который может отправлять пользователям напоминания в виде сообщений в Telegram,
в нужное для пользователя время и дату. Бот имеет базу данных пользователей, нажавших команду `/start`, а также
напоминаний для каждого пользователя.
Бот написан с использованием библиотеки **AIOgram 3.4.1**. Также для создания базы данных задействована библиотека 
**SQLAlchemy 2.0.29**.
___

## Запуск проекта

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/vitalaga/nanny_bot.git
   ```

2. Установите необходимые зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Получите ключи API для бота в Telegram:

    - Если у вас нет бота Telegram, вы можете создать его в [BotFather](https://t.me/botfather) в Telegram. Следуй этим шагам:
     - Откройте Telegram и найдите «BotFather»
     - Начните чат с BotFather и введите команду `/newbot`.
     - Далее BotFather запросит имя для вашего бота.
     - Затем BotFather запросит логин для вашего бота. Логин должен заканчиваться на «bot» (например, «TheBest_bot» или «TheBestBot»).
     - Как только ваш бот будет создан, BotFather предоставит вам токен бота. Сохраните этот токен.
   
4. Настройте бота:

   Откройте файл `main.py` и укажите ваш токен:

   ```python
   bot = Bot("Ваш_токен")
   ```

5. Запустите бота:
   
   ```bash
   python main.py
   ```
---
## Взаимодействие с ботом

При запуске команды `/start` у бота появится клавиатура из трёх кнопок:
1) **Создать напоминание** -
позволяет создать напоминание. Пользователь указывает текст и дату со временем в формате ДД.ММ.ГГГГ ЧЧ:ММ 
*(например: 07.05.2023 21:00)*

2) **Активные напоминания** - присылает пользователю все напоминания, которые ещё не были отправлены ему. 
Ненужные напоминания можно удалить. Для этого под каждым напоминанием имеется кнопка "Удалить"
3) **Контакты** - при нажатии бот отправит вам сообщение со ссылкой на мой профиль GitHub 😋
___
Особенности:
- в качестве бонусной особенности, бот может принимать изображение (фото/картинки) и отправлять их на диск сервера 
(по умолчанию указан путь `D:/`)
- каждые 60 секунд бот проверяет, имеется ли в БД напоминания, которые нужно отправить. 
Интервал можно уменьшить(не рекомендовано) или увеличить.