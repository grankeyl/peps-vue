from aiogram import F, exceptions
from aiogram.types import FSInputFile, InputFile
from aiogram.filters import Command, StateFilter
from aiogram.exceptions import TelegramForbiddenError
from utils import generate_referal_key, get_now_date
from bot.handlers.admin.states import AdminStates
from app import bot, dp

import bot.messages as txt
import bot.view.keyboards as key
import bot.handlers.pillow as pl

from config import cfg
from database.connection import db, User, UserSettings, Skin, UserSkins, UserCosts, Invoices
from routes.user import changeSkinFunc
from io import BytesIO

import datetime
import asyncio
import aiofiles
import os
import random

__all__ = ['dp']

@dp.message(Command("addref"))
async def addref_admin(message, state):
    await state.clear()
    
    uuid_id = str(message.text).split(" ")[1]
    telegramUser = await bot.get_chat(uuid_id)
    telegramUserFirstName = telegramUser.first_name
    telegramUserLastName = telegramUser.last_name
    telegramUserFullName = telegramUser.full_name
    telegramUserUsername = telegramUser.username
    invited_by = "echDe4P0i"
    
    user = User(
        user_id = uuid_id,
        first_name = telegramUserFirstName,
        last_name = telegramUserLastName,
        full_name = telegramUserFullName,
        username = telegramUserUsername,
        photo_id = None,
        invited_by = invited_by,
        join_first = get_now_date()
    )
    
    db.add(user)
    db.flush()
    db.commit()
    
    await bot.send_message(
        message.from_user.id, 
        "Реферал добавлен!"
    )

@dp.message(Command(commands=["admin", "фвьшт", "a", "adm", "ф", "фвь"]))
async def command_start(message, state):
    await state.clear()
    user_id = message.from_user.id
    
    if str(user_id) in str(cfg.get("ADMINS_IDS")):
        await bot.send_message(
            message.from_user.id, 
            txt.TXT_5,
            reply_markup=key.admin()
        )


@dp.callback_query(F.data.startswith("admin:"))
async def command_start(call, state):
    user_id = call.from_user.id
    message_id = call.message.message_id
    data = call.data.split(":")[1]
    
    if str(user_id) in str(cfg.get("ADMINS_IDS")):
        
        if data == "search":
            await bot.edit_message_text(
                text=txt.TXT_15,
                chat_id=user_id, 
                message_id=message_id,
                reply_markup=key.admin_exit()
            )
            
            await state.set_state(AdminStates.search_text)
        
        elif data == "stat":
            users = User.get_all_users()
            users_count = len(users)
            
            users_paid = User.get_all_users_paid()
            users_count_paid = len(users_paid)
            
            users_new_count = User.get_new_users_count()
            users_online_count = User.get_online_count()
            users_online_today_count = User.get_online_today_count()
            total_money = Invoices.get_total_invoice_amount()
            total_money_today = Invoices.get_total_invoice_today_amount()
            
            await bot.edit_message_text(
                text=txt.TXT_3.format(
                    date = get_now_date(),
                    users_count = users_count,
                    users_paid_count = users_count_paid,
                    new_users_count = users_new_count,
                    online_count = users_online_count,
                    online_today_count = users_online_today_count,
                    total_money = int(total_money),
                    total_money_in_dollars = int(total_money) / 100,
                    today_total_money = int(total_money_today),
                    today_money_in_dollars = int(total_money_today) / 100,
                ),
                chat_id=user_id, 
                message_id=message_id,
                reply_markup=key.admin_back()
            )
            
        elif data == "mail":
            
            await bot.edit_message_text(
                text=txt.TXT_6,
                chat_id=user_id, 
                message_id=message_id,
                reply_markup=key.admin_exit()
            )
            
            await state.set_state(AdminStates.mail_text)

        
@dp.message(StateFilter("AdminStates:search_text"))
async def command_start(message, state):

    user_id = message.from_user.id
    
    if message.text.isdigit():
        user = User.get_user(message.text)
    else:
        user = User.get_user_by_username(message.text)
    
    if user is None:
        await bot.send_message(
            user_id, 
            txt.TXT_17,
            reply_markup=key.admin_exit()
        )
    else:
        donates = Invoices.get_total_invoice_amount_user(user["user_id"])
        donates_today = Invoices.get_total_invoice_today_amount_user(user["user_id"])
        
        await bot.send_message(
            user_id, 
            txt.TXT_16.format(
                user_id = user["user_id"],
                full_name = user["full_name"],
                money = user["balance"]["earn"],
                views = user["balance"]["views"],
                ton = user["balance"]["ton"],
                donates = int(donates),
                donates_usd = int(donates) / 100,
                donates_today = int(donates_today),
                donates_today_usd = int(donates_today) / 100
            ),
            reply_markup=key.admin_user_settings(user["user_id"])
        )
        
        await state.clear()


@dp.callback_query(F.data.startswith("user_settings:"))
async def command_start(call, state):
    user_id = call.from_user.id
    message_id = call.message.message_id
    
    data = call.data.split(":")[1]
    data_uuid = call.data.split(":")[2]
    
    if data == "gift_skin":
        await bot.send_message(
            chat_id=user_id, 
            text=txt.TXT_18,
            reply_markup=key.admin_exit()
        )
            
        await state.set_state(AdminStates.search_gift_skin)
        await state.update_data(user_id = data_uuid)
    
    elif data == "gift_money":
        await bot.send_message(
            chat_id=user_id, 
            text=txt.TXT_19,
            reply_markup=key.admin_exit()
        )
        
        await state.set_state(AdminStates.search_gift_money)
        await state.update_data(user_id = data_uuid)
    
    elif data == "gift_views":
        await bot.send_message(
            chat_id=user_id, 
            text=txt.TXT_19,
            reply_markup=key.admin_exit()
        )
        
        await state.set_state(AdminStates.search_gift_views)
        await state.update_data(user_id = data_uuid)


@dp.message(StateFilter("AdminStates:search_gift_skin"))
async def command_start(message, state):
    state_data = await state.get_data()
    user_id_data = state_data["user_id"]
    
    user_id = message.from_user.id
    username = message.from_user.username
    
    user_db_get_settings = UserSettings.get_user(user_id_data)
    
    # add skin to database
    skin = Skin(message.text)
    data_skin = skin.as_dict()
    category_data = skin.category_dict()
                
    user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id_data).first()
    
    if data_skin['baffs']['baffs_type'] is True:
        
        if data_skin['baffs']['baffs_buy_type'] == 'views':
            data_skin['baffs']['baffs_adding_views'] = (user_costs.views_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
            
        elif data_skin['baffs']['baffs_buy_type'] == 'money':
            data_skin['baffs']['baffs_adding_money'] = (user_costs.money_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
            
        elif data_skin['baffs']['baffs_buy_type'] == 'stamina':
            data_skin['baffs']['baffs_adding_stamina'] = (user_costs.stamina_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
        
        elif data_skin['baffs']['baffs_buy_type'] == 'ton':
            user_costs.ton_chance = user_costs.ton_chance + (user_costs.ton_chance / 100 * data_skin['baffs']['baffs_buy_percentage'])
    
    _dataSkin = UserSkins.get_skin(user_id_data, message.text)
                        
    if _dataSkin is None:
        db.add(UserSkins(
            user_id = user_id_data,
            skin_id = message.text,
            skin_category = skin.category,
            skin_rare = data_skin['rare'],
            skin_status = True,
            skin_show = category_data['skin_show'],
            skin_baffs = data_skin['baffs'],
            skin_shop = data_skin['shop_settings'],
            skin_upgrade = data_skin['upgrades_settings']
        ))
    
        await changeSkinFunc(user_id_data, message.text)
    
    db.flush()
    db.commit()
    # add skin to database
    
    await bot.send_message(
        chat_id=user_id,
        text=txt.TXT_22,
        reply_markup=key.admin_exit()
    )
    
    photoBannerCreateData = pl.photoBannerCreate(message.text)
    randomIdPhoto = generate_referal_key()
    
    async with aiofiles.open(f'./bot/handlers/tempmedia/{randomIdPhoto}.jpg', mode='wb') as out_file:
        await out_file.write(photoBannerCreateData)
        
    photo = FSInputFile(f'./bot/handlers/tempmedia/{randomIdPhoto}.jpg')

    await bot.send_photo(
        chat_id=user_id_data,
        photo=photo,
        caption=txt.TXT_23.format(username='@' + username) if user_db_get_settings["language"] == "ru" else txt.TXT_24.format(username=username),
        reply_markup=key.play_menu(user_id_data)
    )
    
    os.remove(f'./bot/handlers/tempmedia/{randomIdPhoto}.jpg')


@dp.message(StateFilter("AdminStates:search_gift_money"))
async def command_start(message, state):
    state_data = await state.get_data()
    user_id_data = state_data["user_id"]
    user_id = message.from_user.id

    userDb = db.query(User).filter(User.user_id == user_id_data).first()

    if str(message.text).startswith(("+", "-", "")) and (str(message.text)[1:].isdigit() or str(message.text) == "0"):
        userDb.update_balance("money", message.text)
        await bot.send_message(
            chat_id=user_id,
            text=txt.TXT_20,
            reply_markup=key.admin_exit()
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text=txt.TXT_21,
            reply_markup=key.admin_exit()
        )

@dp.message(StateFilter("AdminStates:search_gift_views"))
async def command_start(message, state):
    state_data = await state.get_data()
    user_id_data = state_data["user_id"]
    user_id = message.from_user.id

    userDb = db.query(User).filter(User.user_id == user_id_data).first()

    if str(message.text).startswith(("+", "-", "")) and (str(message.text)[1:].isdigit() or str(message.text) == "0"):
        userDb.update_balance("views", message.text)
        await bot.send_message(
            chat_id=user_id,
            text=txt.TXT_20,
            reply_markup=key.admin_exit()
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text=txt.TXT_21,
            reply_markup=key.admin_exit()
        )
        
@dp.message(StateFilter("AdminStates:mail_text"))
async def command_start(message, state):
    user_id = message.from_user.id
    
    await state.update_data(mail_text = str(message.text))
    
    await bot.send_message(
        user_id, 
        txt.TXT_7,
        reply_markup=key.admin_mail_photo()
    )
    
    await state.set_state(AdminStates.mail_photo)
        
@dp.message(StateFilter("AdminStates:mail_photo"))
async def command_start(message, state):
    user_id = message.from_user.id
    
    status_photo = None
    status_video = None
    
    if message.photo:
        await state.update_data(mail_photo = "photo:" + str(message.photo[-1].file_id))
        status_photo = True
    elif message.video:
        await state.update_data(mail_photo = "video:" + str(message.video.file_id))
        status_photo = True
    else:
        status_photo = None
        status_video = None
    
    if status_photo is not None or status_video is not None:
        await bot.send_message(
            user_id, 
            txt.TXT_8,
            reply_markup=key.admin_mail_button()
        )
        
    else:
        await bot.send_message(
            user_id, 
            txt.TXT_11,
            reply_markup=key.admin_exit()
        )


@dp.message(StateFilter("AdminStates:mail_button_text"))
async def command_start(message, state):
    user_id = message.from_user.id
    
    await state.update_data(mail_button_text = str(message.text))
    
    await bot.send_message(
        user_id, 
        txt.TXT_10,
        reply_markup=key.admin_exit()
    )
    
    await state.set_state(AdminStates.mail_button_link)


@dp.message(StateFilter("AdminStates:mail_button_link"))
async def command_start(message, state):
    user_id = message.from_user.id
    
    await state.update_data(mail_button_link = str(message.text))
    
    state_data = await state.get_data()
    mail_text = state_data["mail_text"]
    mail_photo = state_data["mail_photo"]
    mail_button = state_data["mail_button"]
    mail_button_text = state_data["mail_button_text"]
    mail_button_link = state_data["mail_button_link"]
    
    button_status = None
    
    if mail_button is not None:
        button_status = key.button_mail(mail_button_text, mail_button_link)

    if mail_photo is not None:
        if mail_photo.startswith("photo:"):
            await bot.send_photo(
                user_id, 
                photo=mail_photo.split(":")[1],
                caption=mail_text,
                reply_markup=button_status
            )
        elif mail_photo.startswith("video:"):
            await bot.send_video(
                user_id, 
                video=mail_photo.split(":")[1],
                caption=mail_text,
                reply_markup=button_status
            )
            
    elif mail_photo is None:
        await bot.send_message(
            user_id,
            mail_text,
            reply_markup=button_status
        )
        
    
    await bot.send_message(
        user_id,
        txt.TXT_14,
        reply_markup=key.mail_settings_send()
    )
    

@dp.callback_query(F.data == "send_all")
async def command_start(call, state):
    user_id = call.from_user.id
    message_id = call.message.message_id

    users_db_all = User.get_all_users()

    state_data = await state.get_data()
    mail_text = state_data.get("mail_text")
    mail_photo = state_data.get("mail_photo")
    mail_button = state_data.get("mail_button")
    mail_button_text = state_data.get("mail_button_text")
    mail_button_link = state_data.get("mail_button_link")

    button_status = None

    await bot.edit_message_text(
        text=txt.TXT_12,
        chat_id=user_id,
        message_id=message_id
    )

    sent_count = 0
    blocked_count = 0

    if mail_button and mail_button_text and mail_button_link:
        button_status = key.button_mail(mail_button_text, mail_button_link)

    async def send_message_to_user(recipient_id):
        nonlocal sent_count, blocked_count
        try:
            if mail_photo:
                if mail_photo.startswith("photo:"):
                    await bot.send_photo(
                        recipient_id,
                        photo=mail_photo.split(":")[1],
                        caption=mail_text,
                        reply_markup=button_status
                    )
                elif mail_photo.startswith("video:"):
                    await bot.send_video(
                        recipient_id,
                        video=mail_photo.split(":")[1],
                        caption=mail_text,
                        reply_markup=button_status
                    )
            else:
                await bot.send_message(
                    recipient_id,
                    mail_text,
                    reply_markup=button_status
                )
            sent_count += 1
        except TelegramForbiddenError:
            blocked_count += 1

    await asyncio.gather(*(send_message_to_user(i['user_id']) for i in users_db_all))

    await bot.send_message(
        user_id,
        txt.TXT_13.format(
            sent=sent_count,
            blocked=blocked_count
        )
    )
    
    await state.clear()




@dp.callback_query(F.data.startswith("send_channels|"))
async def command_start(call, state):
    user_id = call.from_user.id
    message_id = call.message.message_id
    
    data = call.data.split("|")[1]

    state_data = await state.get_data()
    mail_text = state_data.get("mail_text")
    mail_photo = state_data.get("mail_photo")
    mail_button = state_data.get("mail_button")
    mail_button_text = state_data.get("mail_button_text")
    mail_button_link = state_data.get("mail_button_link")

    button_status = None

    await bot.edit_message_text(
        text=txt.TXT_12,
        chat_id=user_id,
        message_id=message_id
    )
    
    if mail_button and mail_button_text and mail_button_link:
        button_status = key.button_mail(mail_button_text, mail_button_link)

    async def send_message_to_user():
        try:
            if mail_photo:
                if mail_photo.startswith("photo:"):
                    if data == "en":
                        await bot.send_photo(
                            cfg.get("CHANNEL_EN_ID"),
                            photo=mail_photo.split(":")[1],
                            caption=mail_text,
                            reply_markup=button_status
                        )
                    elif data == "ru":
                        await bot.send_photo(
                            cfg.get("CHANNEL_RU_ID"),
                            photo=mail_photo.split(":")[1],
                            caption=mail_text,
                            reply_markup=button_status
                        )
                elif mail_photo.startswith("video:"):
                    if data == "en":
                        await bot.send_video(
                            cfg.get("CHANNEL_EN_ID"),
                            video=mail_photo.split(":")[1],
                            caption=mail_text,
                            reply_markup=button_status
                        )
                    elif data == "ru":
                        await bot.send_video(
                            cfg.get("CHANNEL_RU_ID"),
                            video=mail_photo.split(":")[1],
                            caption=mail_text,
                            reply_markup=button_status
                        )
            else:
                if data == "en":
                    await bot.send_message(
                        cfg.get("CHANNEL_EN_ID"),
                        mail_text,
                        reply_markup=button_status
                    )
                elif data == "ru":
                    await bot.send_message(
                        cfg.get("CHANNEL_RU_ID"),
                        mail_text,
                        reply_markup=button_status
                    )
        except:
            pass

    await send_message_to_user()

    await bot.send_message(
        user_id,
        txt.TXT_13.format(
            sent="Всем в канале",
            blocked="Блокировок нет"
        )
    )
    
    await state.clear()



@dp.callback_query(F.data.startswith("mail_empty:"))
async def command_start(call, state):
    user_id = call.from_user.id
    message_id = call.message.message_id
    data = call.data.split(":")[1]
    
    if str(user_id) in str(cfg.get("ADMINS_IDS")):
        
        if data == "photo":
            await state.update_data(mail_photo = None)
            
            await bot.edit_message_text(
                text=txt.TXT_8,
                chat_id=user_id,
                message_id=message_id,
                reply_markup=key.admin_mail_button()
            )
            
        elif data == "button_empty":
            await state.update_data(mail_button = None)
            await state.update_data(mail_button_text = None)
            await state.update_data(mail_button_link = None)
    
            state_data = await state.get_data()
            mail_text = state_data["mail_text"]
            mail_photo = state_data["mail_photo"]
            mail_button = state_data["mail_button"]
            mail_button_text = state_data["mail_button_text"]
            mail_button_link = state_data["mail_button_link"]
            
            button_status = None
            
            if mail_button is not None:
                button_status = key.button_mail(mail_button_text, mail_button_link)

            if mail_photo is not None:
                if mail_photo.startswith("photo:"):
                    await bot.send_photo(
                        user_id, 
                        photo=mail_photo.split(":")[1],
                        caption=mail_text,
                        reply_markup=button_status
                    )
                elif mail_photo.startswith("video:"):
                    await bot.send_video(
                        user_id, 
                        video=mail_photo.split(":")[1],
                        caption=mail_text,
                        reply_markup=button_status
                    )
                    
            elif mail_photo is None:
                await bot.send_message(
                    user_id,
                    mail_text,
                    reply_markup=button_status
                )
                
            await bot.send_message(
                user_id,
                txt.TXT_14,
                reply_markup=key.mail_settings_send()
            )
            
        elif data == "button_add":
            await state.update_data(mail_button = True)
            
            await bot.edit_message_text(
                text=txt.TXT_9,
                chat_id=user_id,
                message_id=message_id,
                reply_markup=key.admin_exit()
            )
            
            await state.set_state(AdminStates.mail_button_text)




@dp.callback_query(F.data.startswith("admin_back:"))
async def command_start(call, state):
    await state.clear()
    
    user_id = call.from_user.id
    message_id = call.message.message_id
    data = call.data.split(":")[1]
    
    if str(user_id) in str(cfg.get("ADMINS_IDS")):
        
        if data == "admin":
    
            await bot.edit_message_text(
                text=txt.TXT_5,
                chat_id=user_id, 
                message_id=message_id,
                reply_markup=key.admin()
            )
        
        elif data == "exit":
    
            await bot.edit_message_text(
                text=txt.TXT_5,
                chat_id=user_id, 
                message_id=message_id,
                reply_markup=key.admin()
            )