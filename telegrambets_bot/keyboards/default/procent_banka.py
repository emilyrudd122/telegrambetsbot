from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


procent_banka = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='3'),
            KeyboardButton(text='5'),
            KeyboardButton(text='10'),
        ]
    ],
    resize_keyboard=True
)