from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


postim = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет'),
        ]
    ],
    resize_keyboard=True
)