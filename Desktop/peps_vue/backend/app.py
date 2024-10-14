import asyncio
import signal
import uvicorn
import platform
import multiprocessing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiocache import SimpleMemoryCache
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TEST
from config import CreateConfig, cfg

''' CONFIG '''
CreateConfig()

BOT_TOKEN = cfg.get('BOT_TOKEN')

session=AiohttpSession(api=TEST)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
    session=session
)

dp = Dispatcher(storage=MemoryStorage())

''' FastAPI APP '''
app = FastAPI()
cache = SimpleMemoryCache()

''' CORS Middleware '''

if cfg.get("DEVELOPER_STATUS") == True:
    origins = [
        "http://localhost",
        "http://localhost:7000",
        "http://localhost:8080",
        "http://127.0.0.1:7000",
        "http://127.0.0.1:8080",
        "http://185.125.102.222:7000",
        "http://185.125.102.222:8080",
        "http://192.168.0.123:7000",
        "http://192.168.0.123:8080"
    ]
else:
    origins = [
        "http://localhost",
        "http://localhost:7000",
        "http://localhost:8080",
        "http://127.0.0.1:7000",
        "http://127.0.0.1:8080",
        "http://192.168.0.123:7000",
        "http://192.168.0.123:8080",
        "https://5ec6-95-59-121-213.ngrok-free.app",
        "https://29e5a7a9229fa0.lhr.life",
        "http://29e5a7a9229fa0.lhr.life"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.user import router_user
from routes.shop import router_shop
from routes.chest import router_chest
from routes.stars import router_stars
from routes.misc import router as router_misc

import routes.tasks as router_tasks
import routes.daily as router_daily

app.include_router(router_user)
app.include_router(router_shop)
app.include_router(router_misc)
app.include_router(router_chest)
app.include_router(router_stars)
app.include_router(router_tasks.router)
app.include_router(router_daily.router)

''' BOT START '''
async def start_bot():
    try:
        from bot.handlers.user.message import dp
        from bot.handlers.user.payments import dp
        from bot.handlers.admin.message import dp
        
        botted = await bot.get_me()
        print('\x1b[6;30;42m' + 'Бот успешно запущен!' + '\x1b[0m')
        print('\x1b[0;36;40m' + 'Айди' + '\x1b[0m' + " - {u}".format(u=botted.id))
        print('\x1b[0;36;40m' + 'Название' + '\x1b[0m' + " - {u}".format(u=botted.first_name))
        print('\x1b[0;36;40m' + 'Юзернейм' + '\x1b[0m' + " - @{u}".format(u=botted.username))
        print('Логи:' + '\x1b[0m')

        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        
''' UVICORN START '''
def start_uvicorn():
    config = uvicorn.Config(app, host="0.0.0.0", port=7000, reload = True)
    server = uvicorn.Server(config)
    server.run()

''' MAIN FUNCTION '''
async def main():
    loop = asyncio.get_running_loop()

    uvicorn_process = multiprocessing.Process(target=start_uvicorn)
    uvicorn_process.start()

    await router_daily.dailyCreates()
    await router_tasks.taskCreates()
    
    bot_task = loop.create_task(start_bot())

    if platform.system() != "Windows":
        def handler(signum, frame):
            print("Signal handler triggered.")  # Debug print
            bot_task.cancel()
            loop.stop()

        loop.add_signal_handler(signal.SIGINT, handler, signal.SIGINT, None)

    try:
        await bot_task
    except asyncio.CancelledError:
        pass
    finally:
        uvicorn_process.terminate()
        uvicorn_process.join()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass