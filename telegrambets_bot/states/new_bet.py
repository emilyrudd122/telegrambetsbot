from aiogram.dispatcher.filters.state import StatesGroup, State


class Bet(StatesGroup):
    bet_type = State()
    p1 = State()
    p2 = State()
    winner = State()
    winner_map = State()
    coef = State()
    bet = State()
    
    
    
# тип ставки(карта, игра)
# если карта
# п1=п2=карта=винер=кеф=ставка
# если игра
# п1=п2=винер=кеф=ставка