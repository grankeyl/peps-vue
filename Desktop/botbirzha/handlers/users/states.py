import asyncio
from aiogram import types
from database import func
from aiogram.dispatcher import FSMContext
from data import func, mes
from keyboards import defaut as key
from keyboards import inline as menu
from utils.config.config import admin_group
from loader import bot, sd
from utils import *
from keyboards.inline.inline_menu_user import deal_create
from utils.user import User
from states.deals import OpenDeal

@sd.message_handler(state = OpenDeal.card)
async def open_deal(msg: types.Message, state: FSMContext):
    try:
        await msg.answer('<b>Выберите, какая именно нужна вам разработка</b>')
        await OpenDeal.next()
            
    except Exception as e:
		    await bot.send_message(admin_group, f'Пизда, старт наебнулся\n {e}')
  
  
@sd.message_handler(state = OpenDeal.info)
async def open_deal(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            user_id = data['user_id']
            card = data['card']
            id_deal = func.check_deal()
        func.create_deal(id_deal, msg.from_user.id, user_id, card, msg.text)
        await state.finish()
        await bot.send_message(chat_id = msg.from_user.id,
                text = deal_create.format(
                    id_deal = id_deal,
                    buyer = User(msg.from_user.id).username,
                    card = card, info = msg.text,
                    ))
            
    except Exception as e:
		    await bot.send_message(admin_group, f'Пизда, старт наебнулся\n {e}')