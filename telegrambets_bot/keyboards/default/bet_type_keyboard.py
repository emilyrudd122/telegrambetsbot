from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bet_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Лайв'),
            KeyboardButton(text='Линия'),
        ],
    ],
    resize_keyboard=True
)