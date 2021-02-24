from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bet_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Лайв'),
            KeyboardButton(text='Линия'),
        ],
        [
            KeyboardButton(text='Офлайн'),
            
        ],
    ],
    resize_keyboard=True
)