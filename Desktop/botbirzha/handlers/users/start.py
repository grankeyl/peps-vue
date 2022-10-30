from aiogram import types
from database import func
from data.mes.message import cabinet, information, garanter, ordering, deal_site, deal_site_admin, deal_bot, deal_bot_admin, ordering_all, acceptusering, ordering_design_all, deal_design_web, deal_design_web_admin, deal_design_banner, deal_design_banner_admin, deal_design_avatar, deal_design_avatar_admin, deal_design_animate, deal_design_animate_admin
from filters.chat_filters import IsPrivate
from keyboards.default.menu import main_menu, main_menu_btn, admin_sending, admin_sending_btn
from keyboards.inline.inline_menu_user import cabinet_markup, ordering_markup, open_deal_markup, open_deal_design_markup
from keyboards.inline.inline_menu_admin import agree_deal_markup, adm_sending, admin_menu
from loader import bot, sd
import utils
from utils.config.config import admin_group, admin_id
from utils.user import User
import time
import random
from aiogram.dispatcher import FSMContext
from aiogram import types
import sqlite3
from utils import *
from utils.misc import logger
from states.deals import BotDeal, SiteDeal, DesignDealWeb, DesignDealBanner, DesignDealAvatar, DesignDealAnimate
from states.admin import EmailText, EmailPhoto

@sd.message_handler(IsPrivate(), commands=['start'])
async def start_handler(msg: types.Message):
	try:
     
		if msg.from_user.username != None:
			info = func.first_join(msg.from_user.id, msg.from_user.username, msg.text[7:])
			if info[0] != 0:
				await msg.answer(f'<b>Приветствуем вас</b> {msg.from_user.get_mention(as_html=True)}!\n'
                f'В этом боте вы можете заказать разработку проекта, либо дизайн. Мы дорожим своей репутацией и предоставляем наилучшее качество.',
                reply_markup=main_menu())
				await bot.send_message(admin_group, f'Новый пользователь {msg.from_user.get_mention(as_html=True)}')
			else:
				await func.check_user_data(bot, msg.from_user.id)
				await msg.answer(f'{msg.from_user.full_name}, мы рады видеть вас снова, для взаимодействия с ботом вы можете использовать клавиатуру ниже:',
                reply_markup=main_menu())
		else:
			await bot.send_message(chat_id = msg.from_user.id, text = '<b>💢 Вам необходимо установить логин для работы с ботом!</b>')
	except Exception as e:
		await bot.send_message(admin_group, f'Пизда, старт наебнулся\n {e}')

@sd.callback_query_handler(text='admin_info')
async def adm_search(call: types.CallbackQuery):
    if str(call.from_user.id) in str(admin_id):
        await bot.send_message(chat_id = call.from_user.id,
                    text = func.admin_info(), reply_markup = admin_menu())
        await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)
        
@sd.message_handler(IsPrivate(), commands = ['a', 'admin', 'panel'])
async def message_handler(msg: types.Message):
    chat_id = msg.from_user.id
    if str(chat_id) in str(admin_id):
        await bot.send_message(chat_id = chat_id, 
                text = f'{msg.from_user.get_mention(as_html=True)}, панель администратора:',
                reply_markup = admin_menu())


@sd.callback_query_handler(text='email_sending')
async def adm_sendinger(call: types.CallbackQuery):
    if str(call.from_user.id) in str(admin_id):
        await bot.send_message(chat_id = call.from_user.id,
                    text = 'Выберите тип рассылки', reply_markup = adm_sending())

@sd.callback_query_handler(text='email_sending_text')
async def adm_sending_text(call: types.CallbackQuery):
    await EmailText.text.set()
    await call.message.answer('Введите текст рассылки:')

@sd.message_handler(state=EmailText.text)
async def adm_sending_text_1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = msg.text

        await msg.answer(data['text'], parse_mode='html')

        await EmailText.next()
        await bot.send_message(chat_id=msg.from_user.id,
            text='Выбери дальнейшее действие',
            reply_markup=admin_sending())
        
@sd.message_handler(state=EmailText.action)
async def userlisting(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id

    if msg.text in admin_sending_btn:
        if msg.text in admin_sending_btn[0]: # Начать
            users = func.get_users_list()
            start_time = time.time()
            amount_message = 0
            amount_bad = 0

            async with state.proxy() as data:
                text = data['text']
            await state.finish()
            try:
                await bot.send_message(chat_id=chat_id,
                    text=f'✅ Вы запустили рассылку')
            except: pass

            for i in range(len(users)):
                try:
                    await bot.send_message(users[i][0], text, parse_mode='html')
                    amount_message += 1
                except Exception as e:
                    amount_bad += 1
            
            sending_time = time.time() - start_time

            try:
                await bot.send_message(chat_id=chat_id,
                    text=f'✅ Рассылка окончена\n'
                    f'👍 Отправлено: {amount_message}\n'
                    f'👎 Не отправлено: {amount_bad}\n'
                    f'🕐 Время выполнения рассылки - {sending_time} секунд', reply_markup=main_menu())              
            except:pass
        elif msg.text:
            await bot.send_message(chat_id = msg.from_user.id, 
                text='Рассылка отменена')
            await bot.send_message(chat_id = msg.from_user.id, 
                text='Меню админа')
            await state.finish()
        else:   
            await bot.send_message(chat_id = msg.from_user.id, 
                text='Неверная команда, повторите попытку')
            
@sd.callback_query_handler(text='email_sending_photo')
async def adm_sending_photo(call: types.CallbackQuery):
    await EmailPhoto.photo.set()
    await bot.send_message(chat_id = call.from_user.id,
                text = 'Пришлите боту фото, только фото!')


@sd.message_handler(state=EmailPhoto.photo, content_types=['photo'])
async def email_sending_photo_1(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = random.randint(111111111, 999999999)

        await msg.photo[-1].download(f'utils/photos/{data["photo"]}.jpg')
        await EmailPhoto.next()
        await msg.answer('Введите текст рассылки:')
    except:
        await state.finish()
        await msg.answer('ERROR')


@sd.message_handler(state=EmailPhoto.text)
async def email_sending_photo_2(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = msg.text

            with open(f'utils/photos/{data["photo"]}.jpg', 'rb') as photo:

                await msg.answer_photo(photo, data['text'], parse_mode='html')

            await EmailPhoto.next()
            await msg.answer('Выбери дальнейшее действие', reply_markup=admin_sending())
    except:
        await state.finish()
        await msg.answer('⚠️ ERROR')

@sd.message_handler(state=EmailPhoto.action)
async def email_sending_photo_3(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id
    if msg.text in admin_sending_btn:
            if msg.text == admin_sending_btn[0]: # Начать
                users = func.get_users_list()
                start_time = time.time()
                amount_message = 0
                amount_bad = 0

                async with state.proxy() as data:
                    photo_name = data["photo"]
                    text = data["text"]
                await state.finish()
                try:
                    await bot.send_message(chat_id=chat_id,
                        text=f'✅ Вы запустили рассылку',reply_markup=main_menu())
                except: pass

                for i in range(len(users)):
                    try:
                        with open(f'utils/photos/{photo_name}.jpg', 'rb') as photo:
                            await bot.send_photo(chat_id=users[i][0],
                                photo=photo, caption=text,
                                parse_mode='html')
                        amount_message += 1
                    except Exception as e:
                        amount_bad += 1
                
                sending_time = time.time() - start_time

                try:
                    await bot.send_message(chat_id=chat_id,
                        text=f'✅ Рассылка окончена\n'
                        f'👍 Отправлено: {amount_message}\n'
                        f'👎 Не отправлено: {amount_bad}\n'
                        f'🕐 Время выполнения рассылки - {sending_time} секунд', reply_markup=main_menu())              
                except:
                    pass
                
            elif msg.text == admin_sending_btn[1]:
                await state.finish()
                await bot.send_message(msg.from_user.id, 
                    text='Рассылка отменена', reply_markup=main_menu())
                await bot.send_message(msg.from_user.id, 
                    text='Меню админа', reply_markup=admin_menu())
    else:   
            await bot.send_message(msg.from_user.id, 
                text='Не верная команда, повторите попытку', 
                reply_markup=admin_sending())
  
  
@sd.message_handler(IsPrivate(), content_types = ['text'])
async def message_handler(msg: types.Message):
    chat_id = msg.from_user.id

    try:
        
            if msg.text in main_menu_btn[1]:
                try:
                    i = User(chat_id)
                    photo = 'https://i.imgur.com/eCcabJM.png'
                    await bot.send_photo(chat_id = chat_id, photo = photo,
                            caption = cabinet.format(
                                    user_id = chat_id,
                                    login = msg.from_user.get_mention(as_html=True),
                                    data = func.days_stats_users(i.date[:10])),
                            reply_markup = cabinet_markup())
                except Exception as e:
                    utils.misc.logger.error(f'Error Cabinet: {e}')
                    await msg.answer('Ошибка! Введите /start')
                    
                    
            elif msg.text in main_menu_btn[2]:
                await msg.bot.send_message(chat_id = chat_id, 
                            text = information, 
                            disable_web_page_preview=True, )
            
            elif msg.text in main_menu_btn[3]:
                await msg.bot.send_message(chat_id = chat_id, 
                            text = garanter, 
                            disable_web_page_preview=True, )
                
            elif msg.text in main_menu_btn[0]:
                await msg.bot.send_message(chat_id = chat_id, 
                            text = ordering, reply_markup = ordering_markup([0]), 
                            disable_web_page_preview=True, )
                    
            else:
                await msg.answer('<b>🚫 Обработка прошла ужасно. Воспользуйтесь кнопками ниже:</b>')
    except Exception as e:
        print(e)

@sd.callback_query_handler()
async def handler_call(call: types.CallbackQuery, state: FSMContext):
	buyering = call.data.split(":")[len(call.data.split(":")) - 1]
	chat_id = call.from_user.id
	message_id = call.message.message_id
 
	try:
		if call.data == 'site_call':
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id, text = ordering_all,
                    reply_markup = open_deal_markup([0]))
			await bot.send_message(admin_group, f'💻 Пользователь {call.from_user.get_mention(as_html=True)}, заполняет заказ на разработку')
   
		if call.data == 'design_call':
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id, text = ordering_design_all,
                    reply_markup = open_deal_design_markup([0]))
			await bot.send_message(admin_group, f'🏕 Пользователь {call.from_user.get_mention(as_html=True)}, заполняет заказ на дизайн')
   
		if 'confirm' in call.data:
			await bot.send_message(admin_group,
                    text=acceptusering.format(
                        acceptuser = call.from_user.username,
                        buyering = buyering,
                    ), reply_to_message_id=call.message.message_id),
            
			await bot.send_message(chat_id, f'💻 Ваш заказ был принят @{call.from_user.username}, сейчас вам должны написать')

		if 'open_deal_site:' in call.data:
			user_id = call.data.split(":")[1]
			await SiteDeal.card.set()
			async with state.proxy() as data:
				data['user_id'] = user_id
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id,
					text = '<b>Напишите краткое ТЗ (Техническое задание):</b>')
        
		if 'open_deal_bot:' in call.data:
			user_id = call.data.split(":")[1]
			await BotDeal.card.set()
			async with state.proxy() as data:
				data['user_id'] = user_id
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id,
					text = '<b>Напишите краткое ТЗ (Техническое задание):</b>')
   
		if 'open_deal_design_web:' in call.data:
			user_id = call.data.split(":")[1]
			await DesignDealWeb.card.set()
			async with state.proxy() as data:
				data['user_id'] = user_id
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id,
					text = '<b>Напишите краткое ТЗ (Техническое задание):</b>')

		if 'open_deal_design_banner:' in call.data:
			user_id = call.data.split(":")[1]
			await DesignDealBanner.card.set()
			async with state.proxy() as data:
				data['user_id'] = user_id
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id,
					text = '<b>Напишите краткое ТЗ (Техническое задание):</b>')

		if 'open_deal_design_avatar:' in call.data:
			user_id = call.data.split(":")[1]
			await DesignDealAvatar.card.set()
			async with state.proxy() as data:
				data['user_id'] = user_id
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id,
					text = '<b>Напишите краткое ТЗ (Техническое задание):</b>')

		if 'open_deal_design_animate:' in call.data:
			user_id = call.data.split(":")[1]
			await DesignDealAnimate.card.set()
			async with state.proxy() as data:
				data['user_id'] = user_id
			await bot.delete_message(chat_id, message_id)
			await bot.send_message(chat_id = chat_id,
					text = '<b>Напишите краткое ТЗ (Техническое задание):</b>')

	except Exception as e:
		await bot.send_message(admin_group, f'Пизда, старт наебнулся\n {e}')
        
@sd.message_handler(state = SiteDeal.card)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['card'] = msg.text
            await msg.answer('<b>💵 Напишите свой бюджет в долларах на разработку:</b>')
            await SiteDeal.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = SiteDeal.info)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['info'] = msg.text
            await msg.answer('<b>Укажите примеры если есть (Не прикрепляйте скриншоты):</b>')
            await SiteDeal.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = SiteDeal.dealing)
async def open_deal(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        card = data['card']
        info = data['info']
    id_deal = func.check_deal()
    func.create_deal(id_deal, msg.from_user.id, user_id, card, msg.text)
    await state.finish()
    print(data)
    await bot.send_message(chat_id = msg.from_user.id,
            text = deal_site.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text))
    await bot.send_message(admin_group,
            text = deal_site_admin.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text),
            reply_markup = agree_deal_markup())
    
    
    
    
@sd.message_handler(state = BotDeal.card)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['card'] = msg.text
            await msg.answer('<b>💵 Напишите свой бюджет в долларах на разработку:</b>')
            await BotDeal.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = BotDeal.info)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['info'] = msg.text
            await msg.answer('<b>Укажите примеры если есть (Не прикрепляйте скриншоты):</b>')
            await BotDeal.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = BotDeal.dealing)
async def open_deal(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        card = data['card']
        info = data['info']
    id_deal = func.check_deal()
    func.create_deal(id_deal, msg.from_user.id, user_id, card, msg.text)
    await state.finish()
    print(data)
    await bot.send_message(chat_id = msg.from_user.id,
            text = deal_bot.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text))
    await bot.send_message(admin_group,
            text = deal_bot_admin.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text),
            reply_markup = agree_deal_markup())
    


@sd.message_handler(state = DesignDealWeb.card)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['card'] = msg.text
            await msg.answer('<b>💵 Напишите свой бюджет в долларах на разработку:</b>')
            await DesignDealWeb.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealWeb.info)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['info'] = msg.text
            await msg.answer('<b>Укажите примеры если есть (Прикрепите фотографии ссылкой либо через imgur.com):</b>')
            await DesignDealWeb.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealWeb.dealing)
async def open_deal(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        card = data['card']
        info = data['info']
    id_deal = func.check_deal()
    func.create_deal(id_deal, msg.from_user.id, user_id, card, msg.text)
    await state.finish()
    print(data)
    await bot.send_message(chat_id = msg.from_user.id,
            text = deal_design_web.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text))
    await bot.send_message(admin_group,
            text = deal_design_web_admin.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text),
            reply_markup = agree_deal_markup())
    
@sd.message_handler(state = DesignDealBanner.card)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['card'] = msg.text
            await msg.answer('<b>💵 Напишите свой бюджет в долларах на разработку:</b>')
            await DesignDealBanner.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealBanner.info)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['info'] = msg.text
            await msg.answer('<b>Укажите примеры если есть (Прикрепите фотографии ссылкой либо через imgur.com):</b>')
            await DesignDealBanner.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealBanner.dealing)
async def open_deal(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        card = data['card']
        info = data['info']
    id_deal = func.check_deal()
    func.create_deal(id_deal, msg.from_user.id, user_id, card, msg.text)
    await state.finish()
    print(data)
    await bot.send_message(chat_id = msg.from_user.id,
            text = deal_design_banner.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text))
    await bot.send_message(admin_group,
            text = deal_design_banner_admin.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text),
            reply_markup = agree_deal_markup())
    
@sd.message_handler(state = DesignDealAvatar.card)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['card'] = msg.text
            await msg.answer('<b>💵 Напишите свой бюджет в долларах на разработку:</b>')
            await DesignDealAvatar.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealAvatar.info)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['info'] = msg.text
            await msg.answer('<b>Укажите примеры если есть (Прикрепите фотографии ссылкой либо через imgur.com):</b>')
            await DesignDealAvatar.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealAvatar.dealing)
async def open_deal(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        card = data['card']
        info = data['info']
    id_deal = func.check_deal()
    func.create_deal(id_deal, msg.from_user.id, user_id, card, msg.text)
    await state.finish()
    print(data)
    await bot.send_message(chat_id = msg.from_user.id,
            text = deal_design_avatar.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text))
    await bot.send_message(admin_group,
            text = deal_design_avatar_admin.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text),
            reply_markup = agree_deal_markup())
    
@sd.message_handler(state = DesignDealAnimate.card)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['card'] = msg.text
            await msg.answer('<b>💵 Напишите свой бюджет в долларах на разработку:</b>')
            await DesignDealAnimate.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealAnimate.info)
async def open_deal(msg: types.Message, state: FSMContext):
    if msg.text:
            async with state.proxy() as data:
                data['info'] = msg.text
            await msg.answer('<b>Укажите примеры если есть (Прикрепите фотографии ссылкой либо через imgur.com):</b>')
            await DesignDealAnimate.next()
    else:
        await state.finish()
        await msg.answer('<b>Вводить нужно только цифры!</b>')
        
@sd.message_handler(state = DesignDealAnimate.dealing)
async def open_deal(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        card = data['card']
        info = data['info']
    id_deal = func.check_deal()
    func.create_deal(id_deal, msg.from_user.id, user_id, card, msg.text)
    await state.finish()
    print(data)
    await bot.send_message(chat_id = msg.from_user.id,
            text = deal_design_animate.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text))
    await bot.send_message(admin_group,
            text = deal_design_animate_admin.format(
                id_deal = id_deal,
                buyer = msg.from_user.username,
                card = card, info=info, dealing = msg.text),
            reply_markup = agree_deal_markup())
    
