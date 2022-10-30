from asyncio.log import logger
from aiogram import executor
from utils import user

from loader import sd
import handlers
import utils
from utils import *
from utils.misc import logger

if __name__ == '__main__':
	utils.misc.logger.debug('Telegram Bot Active')
	executor.start_polling(sd)