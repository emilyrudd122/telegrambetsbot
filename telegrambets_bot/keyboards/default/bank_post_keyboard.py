from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bank_post_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет'),
        ],
    ],
    resize_keyboard=True
)