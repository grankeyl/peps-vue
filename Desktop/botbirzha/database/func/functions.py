from aiogram import types
import sqlite3
import os
import random
import requests
import json
import datetime
import time
import traceback
from utils import config
from utils.user import *
from keyboards import inline as menu
from data import mes


def connect():
    conn = sqlite3.connect("database/database.db")

    cursor = conn.cursor()

    return conn, cursor

def first_join(user_id, username, code):
    conn, cursor = connect()

    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()
    who_invite = code[7:]

    who_invite = code
    if who_invite == '':
        who_invite = 0
    
    if len(row) == 0:
        users = [f'{user_id}', f'{username}', f'{datetime.datetime.now()}']
        cursor.execute(f'INSERT INTO users VALUES (?,?,?)', users)
        conn.commit()

        return True, who_invite
        
    return False, 0

async def check_user_data(bot, user_id):
    chat = await bot.get_chat(user_id)

    conn, cursor = connect()

    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

    if row[1] != f'{chat.username}':
        cursor.execute(f'UPDATE users SET username = "{chat.username}" WHERE user_id = "{user_id}"')
        conn.commit()
        
def days_stats_users(day):
    a = day.split('-')
    aa = datetime.date(int(a[0]), int(a[1]), int(a[2]))
    today = datetime.date.today()
    cc = today - aa
    dd = str(cc)
    ss = dd.split()[0]
    if ss.split(':')[0] == '0':
        return '1'
    else:
        return ss
    
def check_deal():
    conn, cursor = connect()

    cursor.execute('SELECT COUNT(*) from deal')
    check = cursor.fetchone()[0]

    return check

def create_deal(id_deal, user_id, card_deal, info_deal, bucks_deal):
    conn, cursor = connect()

    deal = [id_deal, user_id, card_deal, info_deal, bucks_deal]
    cursor.execute("INSERT INTO deal (id_deal, user_create, data, card, info) VALUES (?,?,?,?,?)", deal)
    conn.commit()
    
def get_users_list():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users')
    users = cursor.fetchall()

    return users

def admin_info():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM users')
    row = cursor.fetchall()

    amount_user_all = 0

    for i in row:
        amount_user_all += 1


    msg = f"""
🍹 Информаци о пользователях:

🍹 Всего пользователей - <b>{amount_user_all}</b>
"""

    return msg

