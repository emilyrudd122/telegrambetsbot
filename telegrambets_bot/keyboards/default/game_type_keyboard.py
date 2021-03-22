from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


game_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Dota 2'),
            KeyboardButton(text='CS GO'),
        ],
    ],
    resize_keyboard=True
)