from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram.types import ParseMode
import aiogram.utils.markdown as md
from states.new_post import Post
from keyboards.default import postim, menu_keyboard


@dp.message_handler(lambda message: message.text == 'Пост', state=None)
async def cmd_post(message: types.Message):
    markup = types.ReplyKeyboardRemove()

    await Post.start.set()
    
    await message.reply("Что пишем?", reply_markup=markup)

@dp.message_handler(state=Post.start)
async def process_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

    await Post.end.set()
    await message.reply(data['message'])
    await message.reply('Постим?', reply_markup=postim)

@dp.message_handler(lambda message: message.text=='Да', state=Post.end)
async def post_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(
            "@smirnoffbets",
            md.text(data['message']),
            parse_mode=ParseMode.MARKDOWN,
        )
    await message.reply('Запощено!', reply_markup=menu_keyboard)
    await state.finish()
    

@dp.message_handler(lambda message: message.text=='Нет', state=Post.end)
async def dont_post_msg(message: types.Message, state: FSMContext):
    await message.reply('Не запощено!', reply_markup=menu_keyboard)
    await state.finish()