from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot, service, spreadsheetId
from states.new_bet import Bet
from keyboards.default import procent_banka, map_winner, menu_keyboard
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from utils.db_api import db



# TODO: сделать выбор ставок типа на тотал/добавить опции для map4,map5
# TODO: добавить ставка по линии/лайв и сделать выбор: ставка на карту или на фул игру
@dp.message_handler(lambda message: message.text == 'Ставка', state=None)
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
    await message.reply("what  will they win", reply_markup=map_winner)
    

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
        qwe = str(db.get_number())
        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(data['p1'] + "/" + data['p2']),
                md.text(md.bold(data['winner']) + " " + data['winner_map'] + " winner"),
                md.text(data['coef']),
                md.text(data['bet']+"%"),
                md.text("Номер ставки:"+qwe),
                sep='\n',
            ),
            reply_markup=menu_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
        
        coef_excel = data['coef'].replace('.',',')
        yacheika = str(9+int(qwe))
        # проверка номера ставки, если это первая ставка, то вносятся другие данные в первую ячейку
        if(int(qwe) != 1):
            # добавление ставки
            service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
                "data": [
                    {"range": "Лист номер один!B" + yacheika +":H"+yacheika ,
                    "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                    "values": [
                                ["=IF(F%(q)s=\"да\";B%(q)s+E%(q)s;B%(q)s-G%(q)s)"%{"q":int(yacheika)-1}, data['bet'], coef_excel, "=B%s*(C%s/100)*(D%s-1)"%(yacheika, yacheika, yacheika), "", "=B%s*(C%s/100)"%(yacheika, yacheika), "=IF(F%(q)s=\"да\";B%(q)s+E%(q)s;B%(q)s-G%(q)s)"%{"q":yacheika}], # Заполняем первую строку
                            ]}
                ]
            }).execute()
        
        else:
            # добавление ставки
            # здесь в первую ячейку вставляется просто сумма начального банка
            service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
                "data": [
                    {"range": "Лист номер один!B" + yacheika +":H"+yacheika ,
                    "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                    "values": [
                                ["=C1", data['bet'], coef_excel, "=B%s*(C%s/100)*(D%s-1)"%(yacheika, yacheika, yacheika), "", "=B%s*(C%s/100)"%(yacheika, yacheika), "=IF(F%(q)s=\"да\";B%(q)s+E%(q)s;B%(q)s-G%(q)s)"%{"q":yacheika}], # Заполняем первую строку
                            ]}
                ]
            }).execute()

        # обновление ячейки с банком
        service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": "Лист номер один!E1",
                "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": [
                            ["=H"+yacheika], # Заполняем первую строку
                        ]}
            ]
        }).execute()
        print('added bet')
        db.update_number()
        msg = await bot.send_message(
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
        msg_id = msg['message_id']
        db.input_bet(data['p1'], data['p2'], data['winner'], data['winner_map'], data['coef'], data['bet'], msg_id, yacheika)

    # Finish conversation
    await state.finish()
