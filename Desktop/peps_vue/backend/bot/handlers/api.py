from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TEST
from aiogram import Bot, Dispatcher, exceptions
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.exceptions import TelegramAPIError
from config import cfg

import bot.logs as lg

BOT_TOKEN = cfg.get('BOT_TOKEN')

session=AiohttpSession(api=TEST)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
    session=session
)

dp = Dispatcher(storage=MemoryStorage())

async def send_log(type: str, params: dict):
    try:
        if 'user_id' in params:
            if params["user_id"] != "None":
                telegramUser = await bot.get_chat(params["user_id"])
                telegramUserFullName = telegramUser.full_name
            else:
                telegramUserFullName = "Неизвестно"

            if type == "donate":
                await bot.send_message(
                    chat_id=cfg.get("LOGS_CHANNEL_ID"),
                    text=lg.DONATE_1.format(
                        user_id=params["user_id"],
                        full_name=telegramUserFullName,
                        prize=params["prize"],
                        amount=params["amount"],
                    )
                )
        else:
            if type == "error":
                print(params["error"])
                await bot.send_message(
                    chat_id=cfg.get("LOGS_CHANNEL_ID"),
                    text=lg.ERROR_1.format(
                        e=params["error"]
                    )
                )
    except Exception as e:
        print(e)
        pass
    
async def check_subscribe_to_channel(user_id: int, channel_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        
        if str(member.status) in ["ChatMemberStatus.MEMBER", "ChatMemberStatus.ADMINISTRATOR", "ChatMemberStatus.CREATOR"]:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

async def get_user_avatar(user_id: int):
    try:
        photos = await bot.get_user_profile_photos(user_id=user_id, limit=1)
        
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            file = await bot.get_file(file_id)
            
            avatar = await bot.download_file(file.file_path)
            
            return avatar
        else:
            return None
        
    except exceptions.BadRequest as e:
        print(f"Bad Request: {e}")
        return None
        
    except exceptions.TelegramAPIError as e:
        print(f"Telegram API error: {e}")
        return None


class Stars:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def CreateInvoice(
        self,
        invoice_title: str, 
        invoice_description: str,
        invoice_price: str,
        invoice_photo: str,
        invoice_params: dict
    ):

        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print(invoice_title)
        print(invoice_description)
        print(invoice_price)
        print(invoice_photo)
        print(invoice_params)

        link = await bot.create_invoice_link(
            title=invoice_title,
            description=invoice_description,
            payload=str(invoice_params),
            provider_token="",
            currency="XTR",
            prices=[{"amount": invoice_price, "label": invoice_title}],
            photo_url=invoice_photo
        )
        
        print("--------------------")
        print(link)
        print("--------------------")
        
        return link
    
