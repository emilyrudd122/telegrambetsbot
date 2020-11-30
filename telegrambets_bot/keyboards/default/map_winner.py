from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


map_winner = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='map1'),
            KeyboardButton(text='map2'),
            KeyboardButton(text='map3'),
        ]
    ],
    resize_keyboard=True
)