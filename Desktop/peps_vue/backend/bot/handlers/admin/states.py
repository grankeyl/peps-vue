from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    search_text = State()
    search_gift_skin = State()
    search_gift_money = State()
    search_gift_views = State()
    
    mail_text = State()
    mail_photo = State()
    mail_button = State()
    mail_button_text = State()
    mail_button_link = State()