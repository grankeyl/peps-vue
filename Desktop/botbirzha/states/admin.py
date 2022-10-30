from aiogram.dispatcher.filters.state import State, StatesGroup

class EmailText(StatesGroup):
    text = State()
    action = State()

class EmailPhoto(StatesGroup):
    photo = State()
    text = State()
    action = State()