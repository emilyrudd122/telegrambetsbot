from aiogram import types
from aiogram.utils import exceptions
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot, service, spreadsheetId
from states.check_bets import Check_Bets
from keyboards.default import menu_keyboard, winlose_keyboad
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from utils.db_api import db

stavki = []
p1,p2,winner,winner_map,coef,bet,status,post_id,excel_row=0,1,2,3,4,5,6,7,8
@dp.message_handler(lambda message: message.text == 'Ставки', state=None)
async def cmd_check_bets(message: types.Message):
    await Check_Bets.get_bets.set()
    bets = db.get_unmarked_bets()
    
    mes = ""
    i=1
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    
    for b in bets:
        stavki.append(b[post_id])
        mes += "%d) %s/%s #%s# | %s | %s\n" % (i,b[p1], b[p2],b[winner_map], b[coef], b[bet])
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

        stavka_id = stavki[int(data['bet_choice'])-1]
        this_bet = db.get_bet(stavka_id)[0]
        # bet = db.get_bet(stavka_id)
        db.update_bet_status(stavka_id, data['winlose'])
        print('bet %s updated(db)' % (str(stavka_id)))
        excel_win = ''
        if data['winlose'] == 2:
            excel_win = 'Нет'
        elif data['winlose'] == 1:
            excel_win = 'Да'
        service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": "Лист номер один!F"+str(this_bet[excel_row]),
                "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": [
                            [excel_win], # Заполняем первую строку
                ]}
            ]
        }).execute()
        print('bet %s updated(excel)' % (str(stavka_id)))

    
    res = '✅' if data['winlose'] == 1 else '❌'
    # изменение поста со ставкой
    try:
        await bot.edit_message_text(
            md.text(
                md.text(this_bet[p1] + "/" + this_bet[p2]+res),
                md.text(md.bold(this_bet[winner]) + " " + this_bet[winner_map] + " winner"),
                md.text(this_bet[coef]),
                md.text(this_bet[bet]+"%"),
                sep='\n',
            ),
            "@smirnoffbets",
            this_bet[post_id],
            parse_mode=ParseMode.MARKDOWN,
        )
        print('post edited')
    except exceptions.MessageNotModified:
        print("post didnt change")
    
    # TODO: сделать обновление банка в закрепленном посте

    ranges = ["Лист номер один!H25"] # 
            
    results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                        ranges = ranges, 
                                        valueRenderOption = 'FORMATTED_VALUE',  
                                        dateTimeRenderOption = 'FORMATTED_STRING').execute() 
    sheet_values = results['valueRanges'][0]['values']
    bank = sheet_values[0][0]
    
    await bot.edit_message_text(
        md.text(
            md.text("Процент берется всегда от текущего банка."),
            md.text("Все ставки по линии лутбета"),
            md.text("26.11.2020-26.12.2020"),
            md.text("Начальный банк: 100.000р"),
            md.text("Текущий банк: %s" % (bank)),
            sep='\n',
        ),
        "@smirnoffbets",
        6,
        parse_mode=ParseMode.MARKDOWN,
    )
    
    stavki.clear()
    await message.reply("chekiruem", reply_markup=menu_keyboard)
    await state.finish()
 
    
    
    