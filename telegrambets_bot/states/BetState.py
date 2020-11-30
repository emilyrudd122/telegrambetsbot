from aiogram.dispatcher.filters.state import StatesGroup, State


class Bet(StatesGroup):
    p1 = State()
    p2 = State()
    winner = State()
    winner_map = State()
    coef = State()
    bet = State()