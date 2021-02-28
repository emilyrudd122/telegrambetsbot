from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ставка'),
            KeyboardButton(text='Пост'),
            KeyboardButton(text='Банк'),
        ],
        [
            KeyboardButton(text='Ставки'),
        ]
        
    ],
    resize_keyboard=True
)