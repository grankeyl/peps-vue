from app import bot, dp
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError

from database.connection import User, UserSettings

import bot.messages as txt
import bot.view.keyboards as key

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

__all__ = ['dp']


scheduler = AsyncIOScheduler()


# @dp.message(F.chat)
# async def handle_request_chat(message):
#     chat_info = message.forward_from_chat.id
#     print(chat_info)
#     await bot.send_message(message.from_user.id, f"You choose a chanel with ID: {chat_info}")
    
@dp.message(CommandStart())
async def command_start(message, state):
    referrer_id = None
    if len(message.text.split()) > 1:
        referrer_id = message.text.split()[1]
        
    user_id = message.from_user.id
    first_name_user = message.from_user.first_name
    last_name_user = message.from_user.last_name
    full_name_user = message.from_user.full_name
    username_user = message.from_user.username
    language = message.from_user.language_code
    
    if language == "ru":
        language = "ru"
    else:
        language = "en"
    
    photo_start = "https://telegra.ph/file/0ece471fcdc5a3b475076.mp4"
    
    await bot.send_video(
        message.from_user.id,
        video=photo_start,
        caption=txt.TXT_1, 
        reply_markup = key.start_menu(user_id)
    )


async def send_message_cooldown(user_id):
    await bot.send_message(
        user_id, 
        txt.TXT_2, 
        reply_markup = key.max_clicks(user_id)
    )


async def send_message_day():
    users_data = User.get_all_users()
    blocked_count = 0
    
    for i in users_data:
        try:
            user_settings = UserSettings.get_user(i['user_id'])
            language = user_settings['language']
                
            if language == "ru":
                text = "🐸 Пепе хорошенько отдохнул и готов делать посты!"
            else: 
                text = "🐸 Peps is well rested and ready to make posts!"
                
            await bot.send_message(
                i['user_id'], 
                txt.TXT_4.format(msg=text),
                reply_markup=key.play_menu(i['user_id'])
            )
            
        except TelegramForbiddenError:
            blocked_count += 1
        
        except TelegramAPIError:
            pass

scheduler.add_job(send_message_day, CronTrigger(hour=14, minute=00))
scheduler.add_job(send_message_day, CronTrigger(hour=18, minute=00))
scheduler.start()