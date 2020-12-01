from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/bet'),
            KeyboardButton(text='/post'),
        ]
    ],
    resize_keyboard=True
)