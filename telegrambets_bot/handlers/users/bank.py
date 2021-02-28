from aiogram import types
from aiogram.utils import exceptions
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.check_bets import Check_Bets
from keyboards.default import menu_keyboard, winlose_keyboad
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from utils.db_api import db


@dp.message_handler(lambda message: message.text == 'Банк', state=None)
async def send_bank(message: types.Message, state: FSMContext):
    bank = db.get_bank()
    await bot.send_message(
            "@smirnoffbets",
            md.text(
                md.text("Текущий банк: " + str(bank)),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    await message.reply("bank: %s" % bank, reply_markup=menu_keyboard)