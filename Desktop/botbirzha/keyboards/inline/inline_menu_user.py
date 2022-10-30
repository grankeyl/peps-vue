from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import config

def cabinet_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
            [
                InlineKeyboardButton(text = '🛄 Информация', callback_data = 'information_call'),
            ],
		]
	)
 
	return markup

def close_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '💢 Закрыть', callback_data = 'to_close'),
			]
		]
	)

	return markup

def ordering_markup(user_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
            [
                InlineKeyboardButton(text = '💻 Разработка', callback_data = 'site_call'),
            ],
            [
                InlineKeyboardButton(text = '🏕 Дизайн', callback_data = 'design_call'),
            ],
		]
	)
 
	return markup

def open_deal_markup(user_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '🖥 Сайт', callback_data = f'open_deal_site:{user_id}'),
			],
            [
                InlineKeyboardButton(text = '⚙️ Бот', callback_data = f'open_deal_bot:{user_id}'),
            ]
		]
	)

	return markup

def open_deal_design_markup(user_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '📱 Веб-дизайн', callback_data = f'open_deal_design_web:{user_id}'),
			],
            [
                InlineKeyboardButton(text = '🌇 Баннер', callback_data = f'open_deal_design_banner:{user_id}'),
            ],
            [
                InlineKeyboardButton(text = '⛺️ Аватарка', callback_data = f'open_deal_design_avatar:{user_id}'),
            ],
            [
                InlineKeyboardButton(text = '📸 Анимация', callback_data = f'open_deal_design_animate:{user_id}'),
            ]
		]
	)

	return markup