from aiogram.dispatcher.filters.state import StatesGroup, State


class Post(StatesGroup):
    start = State()
    end = State()