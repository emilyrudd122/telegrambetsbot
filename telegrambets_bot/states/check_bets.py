from aiogram.dispatcher.filters.state import StatesGroup, State


class Check_Bets(StatesGroup):
    get_bets = State()
    status = State()
    complete = State()