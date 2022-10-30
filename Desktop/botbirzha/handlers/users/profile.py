from aiogram import types
from database import func
from app import get_profpic
from filters.chat_filters import IsPrivate
from keyboards.default.menu import main_menu, main_menu_btn
from keyboards.inline.inline_menu_user import cabinet_markup
from loader import bot, sd
from message import cabinet
from utils.config import config
from utils.user import User
from os import remove
import utils
from utils import *
from utils.misc import logger

@sd.message_handler(IsPrivate(), content_types = ['text'])
async def message_handler(msg: types.Message):
    chat_id = msg.from_user.id

    try:
            if msg.text in main_menu_btn[1]:
                    i = User(chat_id)
                    photo = await get_profpic(msg.from_user.username) if msg.from_user.username else 'https://imgur.com/b9DqKpA.png'
                    p = types.InputFile(photo) if photo is not None else 'https://imgur.com/b9DqKpA.png'
                    await bot.send_photo(chat_id = chat_id, photo = p,
                            caption = cabinet.format(
                                    user_id = chat_id,
                                    login = msg.from_user.get_mention(as_html=True)),
                            reply_markup = cabinet_markup())
                    s = remove(photo) if photo is not None else None
            else:
                await msg.answer('<b>🚫 Обработка прошла ужасно. Воспользуйтесь кнопками ниже:</b>', reply_markup = main_menu())
    except Exception as e:
	    await bot.send_message(config.config('admin_group'), f'Пизда, старт наебнулся\n {e}')