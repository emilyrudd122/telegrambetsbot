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

# TODO: сделать добавление пост_ид для ставок которые добавлены через офлайн режим

p1,p2,winner,winner_map,coef,bet,status,post_id,game_type=0,1,2,3,4,5,6,7,8
@dp.message_handler(lambda message: message.text == 'Ставки', state=None)
async def cmd_check_bets(message: types.Message, state: FSMContext):
    await Check_Bets.get_bets.set()
    bets = db.get_unmarked_bets()
    if not bets:
        await bot.send_message(message.chat.id, "no bets", reply_markup=menu_keyboard)
        await state.finish()
        return
    async with state.proxy() as data:
        data['stavki'] = []
    mes = ""
    i=1
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    
    for b in bets:
        async with state.proxy() as data:
            data['stavki'].append(b[post_id])
        xd = "р."
        mes += "%d) %s/%s <%s> | %s | %s%s \n" % (i,b[p1], b[p2],b[winner_map], b[coef], b[bet], xd)
        i+=1
        
    for a in range(1,i):
        markup.add(str(a))
        
    await bot.send_message(
        message.chat.id,
        mes,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )
        
@dp.message_handler(state=Check_Bets.get_bets)
async def set_status(message:types.Message, state: FSMContext):
    await Check_Bets.status.set()
    async with state.proxy() as data:
        data['bet_choice'] = message.text
    

    await message.reply("Ставка зашла или нет? ", reply_markup=winlose_keyboad)

@dp.message_handler(state=Check_Bets.status)
async def check_status(message:types.Message, state: FSMContext):
    # await Check_Bets.complete.set()
    async with state.proxy() as data:
        if message.text == 'lose❌':
            data['winlose'] = 2
        else:
            data['winlose'] = 1

        stavka_id = data['stavki'][int(data['bet_choice'])-1]
        this_bet = db.get_bet(stavka_id)[0]
        # bet = db.get_bet(stavka_id)
        db.update_bet_status(stavka_id, data['winlose'])
        print('bet %s updated(db)' % (str(stavka_id)))

    
    res = '✅' if data['winlose'] == 1 else '❌'
    # изменение поста со ставкой
    try:
        await bot.edit_message_text(
            md.text(              
                md.text(md.bold(this_bet[game_type]) + " " + res + res),
                md.text(),
                md.text(this_bet[p1] + " vs " + this_bet[p2]),
                md.text(md.bold(this_bet[winner]) + " " + this_bet[winner_map] + " winner"),
                md.text(),
                md.text(this_bet[coef]),
                md.text(this_bet[bet]+"р."),
                sep='\n',
            ),
            "@smirnoffbets",
            this_bet[post_id],
            parse_mode=ParseMode.MARKDOWN,
        )
        print('post edited')
    except exceptions.MessageNotModified:
        print("post didnt change")
    
    if data['winlose'] == 1:
        summa = float(this_bet[bet])*float(this_bet[coef])
        db.update_bank(summa)
        
    
    # stavki.clear()
    await message.reply("chekiruem", reply_markup=menu_keyboard)
    await state.finish()
 
    
    
    