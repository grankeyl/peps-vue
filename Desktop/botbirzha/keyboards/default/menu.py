from aiogram import types
import sqlite3
from database import func


main_menu_btn = [
    '💶 Сделать заказ',
    '🗝 Кабинет',
    '📖 Информация',
    '🛡 Гарантии',
]

admin_sending_btn = [
    '✅ Начать',
    '💢 Отмена',
]


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        main_menu_btn[0],
        main_menu_btn[1],
    )
    markup.add(
        main_menu_btn[2],
        main_menu_btn[3],
    )

    return markup

def admin_sending():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        admin_sending_btn[0],
        admin_sending_btn[1],
    )

    return markup

admin_sending_btn = [
    '✅ Начать',
    '💢 Отмена',
]

def admin_sending():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        admin_sending_btn[0],
        admin_sending_btn[1],
    )

    return markup