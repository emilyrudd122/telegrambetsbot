from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


procent_banka = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='300'),
            KeyboardButton(text='500'),
            KeyboardButton(text='1000'),
        ]
    ],
    resize_keyboard=True
)