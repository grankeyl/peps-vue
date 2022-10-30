from aiogram.dispatcher.filters.state import State, StatesGroup

class SiteDeal(StatesGroup):
    user_id = State()
    card = State()
    info = State()
    dealing = State()
    
class BotDeal(StatesGroup):
    user_id = State()
    card = State()
    info = State()
    dealing = State()
    
class DesignDealWeb(StatesGroup):
    user_id = State()
    card = State()
    info = State()
    dealing = State()

class DesignDealBanner(StatesGroup):
    user_id = State()
    card = State()
    info = State()
    dealing = State()

class DesignDealAvatar(StatesGroup):
    user_id = State()
    card = State()
    info = State()
    dealing = State()

class DesignDealAnimate(StatesGroup):
    user_id = State()
    card = State()
    info = State()
    dealing = State()