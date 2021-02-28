from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.new_bet import Bet
from keyboards.default import procent_banka, map_winner, menu_keyboard, bet_type_keyboard, game_type_keyboard
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from utils.db_api import db



# TODO: сделать выбор ставок типа на тотал/добавить опции для map4,map5
# TODO: сделать выбор постить банк в канал или нет
@dp.message_handler(lambda message: message.text == 'Ставка', state=None)
async def cmd_bet(message: types.Message):
    await Bet.bet_type.set()
    markup = bet_type_keyboard

    await message.reply("Ставка по линии или лайв?", reply_markup=markup)

@dp.message_handler(state=Bet.bet_type)
async def get_type(message: types.Message, state: FSMContext):
    await Bet.game_type.set()
    async with state.proxy() as data:
        data['bet_type'] = message.text
    markup = game_type_keyboard
    await message.reply("Что за игра?", reply_markup=markup)

@dp.message_handler(state=Bet.game_type)
async def get_p1(message: types.Message, state: FSMContext):
    await Bet.p1.set()
    async with state.proxy() as data:
        data['game_type'] = message.text
    markup = types.ReplyKeyboardRemove()
    await message.reply("Первая команда", reply_markup=markup)
    
@dp.message_handler(state=Bet.p1)
async def process_p1(message: types.Message, state: FSMContext):
    """
    Process p1
    """
    async with state.proxy() as data:
        data['p1'] = message.text

    await Bet.p2.set()
    await message.reply("Вторая команда")
    
@dp.message_handler(state=Bet.p2)
async def process_p2(message: types.Message, state: FSMContext):
    """
    Process p2
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    async with state.proxy() as data:
        data['p2'] = message.text
        markup.add(data['p1'], data['p2'])
    await Bet.winner.set()
    await message.reply("Кто победит?", reply_markup=markup)
    
@dp.message_handler(state=Bet.winner)
async def process_winner(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['winner'] = message.text
    await Bet.winner_map.set()
    await message.reply("На какой карте или в игре?", reply_markup=map_winner)
    

@dp.message_handler(state=Bet.winner_map)
async def process_winner_map(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['winner_map'] = message.text
    await Bet.coef.set()
    markup = types.ReplyKeyboardRemove()
    await message.reply("Коэффициент (exxmpl: 1.54)", reply_markup=markup)
    
@dp.message_handler(state=Bet.coef)
async def process_coef(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['coef'] = message.text
    await Bet.bet.set()
    await message.reply("Размер ставки (в рублях)", reply_markup=procent_banka)
    
    
    
@dp.message_handler(state=Bet.bet)
async def process_bet(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bet'] = message.text
        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(data['p1'] + "/" + data['p2']),
                md.text(md.bold(data['winner']) + " " + data['winner_map'] + " winner"),
                md.text(data['coef']),
                md.text(data['bet']+"р."),
                sep='\n',
            ),
            reply_markup=menu_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
            
        msg = await bot.send_message(
            "@smirnoffbets",
            md.text(
                md.text(md.bold(data['game_type'] + " " + data['bet_type'])),
                md.text(),
                md.text(data['p1'] + " vs " + data['p2']),
                md.text(md.bold(data['winner']) + " " + data['winner_map'] + " winner"),
                md.text(),
                md.text(data['coef']),
                md.text(data['bet']+"р."),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

        print('added bet')
        msg_id = msg['message_id']
        db.update_bank(data['bet'], "minus")
        db.input_bet(data['p1'], data['p2'], data['winner'], data['winner_map'], data['coef'], data['bet'], msg_id, data['game_type'])

    # Finish conversation
    await state.finish()
