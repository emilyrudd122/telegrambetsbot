from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram.types import ParseMode
import aiogram.utils.markdown as md



@dp.message_handler(Command("post"), state=None)
async def cmd_bet(message: types.Message):
    markup = types.ReplyKeyboardRemove()

    await message.reply("Hi there! Who is p1", reply_markup=markup)