from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


map_winner = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='map1'),
            KeyboardButton(text='map2'),
            KeyboardButton(text='map3'),
        ],
        [
            KeyboardButton(text='game'),
        ],
    ],
    resize_keyboard=True
)