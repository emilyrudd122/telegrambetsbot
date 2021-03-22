from aiogram import types
from aiogram.utils import exceptions
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.bank_post import Bank_post
from keyboards.default import menu_keyboard, bank_post_keyboard
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from utils.db_api import db


@dp.message_handler(lambda message: message.text == 'Банк', state=None)
async def check_bank(message: types.Message, state: FSMContext):
    await Bank_post.post.set()

    await message.reply("Запостить в канал?: ", reply_markup=bank_post_keyboard)
    
@dp.message_handler(state=Bank_post.post)
async def post_bank(message: types.Message, state: FSMContext):
    bank = db.get_bank()
    if message.text.lower() == "да":
        await bot.send_message(
            "@smirnoffbets",
            md.text(
                md.text("Текущий банк: " + str(bank)),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    await state.finish()
    await message.reply("Текущий банк: %s " % bank, reply_markup=menu_keyboard) 