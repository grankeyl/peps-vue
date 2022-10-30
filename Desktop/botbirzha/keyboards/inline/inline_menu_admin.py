from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import config

def agree_deal_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '✅ Подтвердить заказ', callback_data = 'confirm'),
			],
            [
                InlineKeyboardButton(text = '❌ Отказаться от заказа', callback_data = 'decline'),
            ]
		]
	)

	return markup

def agree_type_deal_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '🖋 Написать заказчику', callback_data = 'dfds'),
			],
		]
	)

	return markup

def admin_menu():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = 'Статистика', callback_data = 'admin_info'),
                InlineKeyboardButton(text = 'Рассылка', callback_data = 'email_sending'),
			],
		]
	)

	return markup

def adm_sending():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '✔️ Рассылка(только текст)', callback_data = 'email_sending_text'),
			],
			[
				InlineKeyboardButton(text = '✔️ Рассылка(текст + фото)', callback_data = 'email_sending_photo'),
			]
		]
	)

	return markup