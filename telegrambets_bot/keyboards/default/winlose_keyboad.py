from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


winlose_keyboad = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='lose❌'),
            KeyboardButton(text='win✅'),
        ]
    ],
    resize_keyboard=True
)