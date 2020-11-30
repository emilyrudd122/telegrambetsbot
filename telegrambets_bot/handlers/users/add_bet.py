from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.BetState import Bet
from keyboards.default import procent_banka, map_winner
from aiogram.types import ParseMode
import aiogram.utils.markdown as md



@dp.message_handler(Command("bet"), state=None)
async def cmd_bet(message: types.Message):
    await Bet.p1.set()
    markup = types.ReplyKeyboardRemove()

    await message.reply("Hi there! Who is p1", reply_markup=markup)
    
@dp.message_handler(state=Bet.p1)
async def process_p1(message: types.Message, state: FSMContext):
    """
    Process p1
    """
    async with state.proxy() as data:
        data['p1'] = message.text

    await Bet.p2.set()
    await message.reply("who is p2")
    
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
    await message.reply("who will win", reply_markup=markup)
    
@dp.message_handler(state=Bet.winner)
async def process_winner(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['winner'] = message.text
    await Bet.winner_map.set()
    await message.reply("Which map will they win", reply_markup=map_winner)
    

@dp.message_handler(state=Bet.winner_map)
async def process_winner_map(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['winner_map'] = message.text
    await Bet.coef.set()
    markup = types.ReplyKeyboardRemove()
    await message.reply("kakoi coef (exxmpl: 1.54)", reply_markup=markup)
    
@dp.message_handler(state=Bet.coef)
async def process_coef(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['coef'] = message.text
    await Bet.bet.set()
    await message.reply("procent banka", reply_markup=procent_banka)
    
@dp.message_handler(state=Bet.bet)
async def process_bet(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bet'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardMarkup()
        markup.add('/bet')

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(data['p1'] + "/" + data['p2']),
                md.text(md.bold(data['winner']) + " " + data['winner_map'] + " winner"),
                md.text(data['coef']),
                md.text(data['bet']+"%"),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        await bot.send_message(
            "@smirnoffbets",
            md.text(
                md.text(data['p1'] + "/" + data['p2']),
                md.text(md.bold(data['winner']) + " " + data['winner_map'] + " winner"),
                md.text(data['coef']),
                md.text(data['bet']+"%"),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()
