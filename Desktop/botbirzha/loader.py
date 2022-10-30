from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.config.config import bot_token

bot = Bot(bot_token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
sd = Dispatcher(bot, storage=storage)