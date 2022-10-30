import logging
from pymongo import MongoClient
import certifi
import threading
from pathlib import Path
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from datetime import timedelta, datetime
from aiogram.dispatcher.filters.builtin import CommandStart, ChatTypeFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery
from aiogram.utils import executor
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData

TOKEN = "5171613069:AAHen86_3BtQE20RvyL-zWuxQVsGwBTPW0g"
admin_chat_id = -1001641770664
admins_id = [5557202913]

cluster = MongoClient("mongodb+srv://nickework:nickework223@cluster0.ig5au4d.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

db = cluster['Guide1']
workers = db['workers']

def f():
  threading.Timer(20.0, f).start()  # Перезапуск через 5 секунд
  print("This Is Worked!")

f()

# Создаём бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
# Присваиваем хранилище переменной storage, оно нам понадобится позже.
storage = MemoryStorage()
# Создаём диспетчер с аргументами bot и storage
dp = Dispatcher(bot, storage=storage)
# Добавляем встроенную миддлварь для удобного логгирования
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

# Пропишем простую клавиатуру Зарегистрироваться из одной кнопки
reg_button = KeyboardButton("🖥 Заказать сайт")
reger_button = KeyboardButton("💎 Заказать дизайн")
info_button = KeyboardButton("⚙️ Профиль")
price_button = KeyboardButton("📄 Прайс-лист")
works_button = KeyboardButton("💎 Портфолио")
reg_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
reg_keyboard.add(reg_button, reger_button, info_button, price_button, works_button)

site_button_card_one = KeyboardButton("Лендинг")
site_button_card_two = KeyboardButton("Многостраничник")
site_button_card_three = KeyboardButton("Сайт-визитка")
site_button_card_four = KeyboardButton("Корпоративный сайт")
site_button_card_five = KeyboardButton("Интернет-магазин")
site_button_card_six = KeyboardButton("Обменник")
site_button_card_seven = KeyboardButton("Другое")
cancel_button = KeyboardButton("◀️ Отмена")
site_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
site_keyboard.add(site_button_card_one, site_button_card_two, site_button_card_three, site_button_card_four, site_button_card_five, site_button_card_six, site_button_card_seven, cancel_button)

# design_button_card_one = KeyboardButton("Low Plan")
# design_button_card_two = KeyboardButton("Middle Plan")
# design_button_card_three = KeyboardButton("Grand Plan")
# design_button_card_four = KeyboardButton("Fantastic Plan")
# cancel_button = KeyboardButton("◀️ Отмена")
# design_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# design_keyboard.add(design_button_card_one, design_button_card_two, design_button_card_three, design_button_card_four, cancel_button)

design_button_tarif_card_one = KeyboardButton("Аватарка")
design_button_tarif_card_two = KeyboardButton("Баннер")
design_button_tarif_card_three = KeyboardButton("Промо-ролик")
design_button_tarif_card_four = KeyboardButton("Анимация")
design_button_tarif_card_five = KeyboardButton("Веб-дизайн")
design_button_tarif_card_six = KeyboardButton("Оформление соц.сетей")
cancel_button = KeyboardButton("◀️ Отмена")
design_tarif_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
design_tarif_keyboard.add(design_button_tarif_card_one, design_button_tarif_card_two, design_button_tarif_card_three, design_button_tarif_card_four, design_button_tarif_card_five, design_button_tarif_card_six, cancel_button)

# Пропишем простую клавиатуру Отмена из одной кнопки
note_button = InlineKeyboardButton("Отказ ❌", callback_data='button1')
yes_button = InlineKeyboardButton("Принять ✅", callback_data='button2')
vote_keyboard = InlineKeyboardMarkup()
vote_keyboard.add(note_button, yes_button)

noter_button = InlineKeyboardButton("Удалить ❌", callback_data='buttoner1')
voter_keyboard = InlineKeyboardMarkup()
voter_keyboard.add(noter_button)

# Задаём параметры Callback данных
reg_callback = CallbackData("reg", "status", "chat_id")

# Оборачиваем клаву в функцию, чтобы было удобнее использовать.
def inline(chat_id):
    cancel = InlineKeyboardButton(
        text="Отказ ❌",
        callback_data=reg_callback.new(
            status="1", chat_id=chat_id
        ),
    )
    confirm = InlineKeyboardButton(
        text="Принять ✅",
        callback_data=reg_callback.new(
            status="2", chat_id=chat_id
        ),
    )
    conf_inline = InlineKeyboardMarkup()
    conf_inline.insert(cancel).insert(confirm)
    return conf_inline

def inlineaccept(chat_id):
    acceptbdd = InlineKeyboardButton(
        text="Я согласен ✅",
        callback_data=reg_callback.new(
            status="3", chat_id=chat_id,
        ),
    )
    conf_inline = InlineKeyboardMarkup()
    conf_inline.insert(acceptbdd)
    return conf_inline


@dp.callback_query_handler(reg_callback.filter(status="3"))
async def accept(call: CallbackQuery, callback_data: dict):
    await call.answer()
    print(call.message.message_id, "conf")
    await call.message.edit_reply_markup()
    await bot.delete_message(
            call.message.chat.id, call.message.message_id
    )
    await bot.send_message(
        call.message.chat.id, "<b>Приветствуем в боте BrainOrUx Studio, здесь ты можешь заказать дизайн любой сложности.</b>\n\nКлавиатура доступна ниже:", reply_markup=reg_keyboard
    )
    # Добавляем работника в БД
    workers.insert_one(
        {
            "_id": int(callback_data.get("chat_id")),
        }
    )

@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button1(call: CallbackQuery):
    # Редачим сообщение в чате админов
    await bot.edit_message_text(
        f"Заказ был принят @{call.from_user.username}\n\n", admin_chat_id, call.message.message_id, reply_markup=voter_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'buttoner1')
async def process_callback_button1(call: CallbackQuery):
    # Редачим сообщение в чате админов
    await bot.delete_message(
       admin_chat_id, call.message.message_id
    )

#
# @dp.callback_query_handler(lambda c: c.data == 'button2')
# # callback данные мы сразу же приобразуем в словарь для удобства работы
# async def decline(callback_query: types.CallbackQuery):
#     await callback_query.answer()
#     # Редачим сообщение в чате админов
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(
#         "Хуйлан нажал кнопку принять теперь заказ его сосунки!.", callback_query.message.message_id
#     )
#     # Отправляем вердикт.
#     await bot.send_message(int(callback_query.get("chat_id")), "Увы и ах, иди ка ...")

cancel_button = KeyboardButton("◀️ Отмена")
profile3_button = KeyboardButton("📚 Помощь")
profilegroup_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
profilegroup_keyboard.add(profile3_button, cancel_button)

cancel_button = KeyboardButton("◀️ Отмена")
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(cancel_button)


# Создаём класс, передаём в него StatesGroup, он нам понадобится, чтобы провести юзера через анкету
# и сохранить каждый ответ. Если кто-то хочет почитать поподробнее, загуглите "aiogram машина состояний"
class Programming(StatesGroup):
    # внутри объявляем Стейты(состояния), далее мы будем вести пользователя по цепочке этих стейтов
    name = State()
    age = State()
    example = State()
    money = State()
    end = State()


class Design(StatesGroup):
    # внутри объявляем Стейты(состояния), далее мы будем вести пользователя по цепочке этих стейтов
    name = State()
    age = State()
    lac = State()
    photo = State()
    money = State()
    end = State()


# banned_users = set()


# @dp.message_handler(user_id=banned_users)
# async def handle_banned(message: types.Message, state: FSMContext):
#     print(f"{message.from_user.username} пишет, но мы ему не ответим!")
#     return True
    

# @dp.message_handler(Text(equals="/ban")) # здесь укажи свой ID
# async def handle_ban_command(message: types.Message, state: FSMContext):
#     # проверяем, что ID передан правильно
#     try:
#         abuser_id = int(message.get_args())
#     except (ValueError, TypeError):
#         return await message.reply("Укажи ID пользователя.")
    
#     banned_users.add(abuser_id)
#     await message.reply(f"Пользователь {abuser_id} заблокирован.")

# Начнём писать хэндлеры для сообщений, сначала пропишем хэндлер для команды /start
# Теперь пропишем цепочку хэндлеров для анкеты

@dp.message_handler(Text(equals="/start"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.chat.id == admin_chat_id:
        if message.from_user.username:
            await bot.send_message(
                message.chat.id, "Ошибка! Для продолжения вы должны написать боту", reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            await bot.send_message(
                message.chat.id, "Ошибка! Для продолжения вы должны поставить юзернейм", reply_markup=types.ReplyKeyboardRemove()
            )

    else:
        await bot.send_message(
            message.chat.id, "Приветствуем в боте BrainOrUx Studio, здесь ты можешь заказать дизайн любой сложности.\n\n<b>Ознакомься с правилами ниже для продолжения:</b>\n\n<pre>1) Возврат денег за заказы не предусмотрены</pre>\n<pre>2) Вывод средств предусмотрен только в крайних случаях</pre>",
            reply_markup=inlineaccept(
            f"{message.chat.id}",
            ),
        )

@dp.message_handler(Text(equals="Портфолио"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        await bot.send_message(
            message.chat.id, f'<b>Ваш профиль</b> \n\n<b>Ваш юзернейм:</b> @{message.from_user.username}\n<b>Ваш айди:</b> @{message.from_user.id}\n<b>Количество заказов:</b> 0', reply_markup=profilegroup_keyboard
        )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message_handler(Text(equals="⚙️ Профиль"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        await bot.send_message(
            message.chat.id, f'<b>⚙️ Ваш профиль</b>\n\n<b>✏️ Ваш юзернейм:</b> @{message.from_user.username}\n<b>🔒 Ваш айди:</b> @{message.from_user.id}', reply_markup=profilegroup_keyboard
        )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message_handler(Text(equals="📚 Помощь"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        await bot.send_message(
            message.chat.id, f'<b>👑 Администратор проекта:</b> @grankeyl, @inject_dev\n<b>🛠 По вопросам/жалобам:</b> @grankeyl, @inject_dev\n<b>💸 Проблема с заказом:</b> @godot_maiden', reply_markup=profilegroup_keyboard
        )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message_handler(Text(equals="📄 Прайс-лист"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        # await bot.send_message(
        #     message.chat.id, f'<b>💸 Прайс-лист:</b>\n\n<b>• Лендинг - От 150$ (цена зависит от сложности и количества блоков на странице)</b>\n<b>• Многостраничник - От 300$ (цена зависит от количества страниц)</b>\n<b>• Интернет-магазин - От 800$ (цена зависит от сложности функций)</b>\n\n‼️ Цена может быть намного ниже, все зависит от сложности задания, все детали обговариваются отдельно!', reply_markup=profilegroup_keyboard
        # )
        await bot.send_message(
            message.chat.id, f'<b>Данный раздел на техническом обслуживании!</b>', reply_markup=profilegroup_keyboard
        )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message_handler(Text(equals="💎 Портфолио"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        await bot.send_message(
            message.chat.id, f'<b>🖥 Портфолио доступно по ссылкам ниже:</b>\n\n<b>Портфолио с сайтами: @brainorux_russian, @brainorux_channel</b>\n<b>Портфолио с дизайном: @brainorux_design</b>', reply_markup=profilegroup_keyboard
        )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )

# Прописываем handler для кнопки отмены, мы заканчиваем State и возвращаем юзера в главное меню
# Продумывайте порядок написания handlerов так как они работают с верху в низ.
@dp.message_handler(Text(equals="◀️ Отмена"), state="*")
async def menu_button(message: types.Message, state: FSMContext):
    if message.from_user.username:
        await state.finish()
        await bot.send_message(
        message.chat.id, "<b>Вы вернулись в меню.</b>", reply_markup=reg_keyboard
        )
    else:
        await bot.send_message(
            message.chat.id, "Ошибка! Для продолжения вы должны поставить юзернейм.", reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message_handler(Text(equals="🖥 Заказать сайт"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        await state.update_data(name=message.text)
        await bot.send_message(
            message.chat.id, "<b>Укажите тип сайта который вам нужен:</b>", reply_markup=site_keyboard
        )
        await Programming.age.set()
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
        await Programming.age.set()

@dp.message_handler(state=Programming.age, content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
    # Записываем ответ в storage
        await state.update_data(lac=message.text)
        await bot.send_message(
        message.chat.id, "<b>Опишите кратко техническое задание (Прикрепляйте картинки при необходимости):</b>", reply_markup=cancel_keyboard
    )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
    await Programming.money.set()

@dp.message_handler(state=Programming.money, content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
    # Записываем ответ в storage
        await state.update_data(money=message.text)
        await bot.send_message(
        message.chat.id, "<b>Укажите свой бюджет:</b>", reply_markup=cancel_keyboard
    )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
    await Programming.example.set()

@dp.message_handler(state=Programming.example, content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
    # Записываем ответ в storage
        await state.update_data(example=message.text)
        await bot.send_message(
        message.chat.id, "<b>Укажите примеры сайтов:</b>", reply_markup=cancel_keyboard
    )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
    await Programming.end.set()


@dp.message_handler(state=Programming.end, content_types=types.ContentTypes.TEXT)
async def confirmation(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await bot.send_message(
        message.chat.id, "<b>Анкета успешно заполнена, после проверки вы получите ответ.</b>", reply_markup=reg_keyboard
    )
    await bot.send_message(
        admin_chat_id,
        text = f"<b>💻 Новая заявка от </b>@{message.from_user.username}\n➖➖➖➖➖➖➖➖➖➖\n"f'<b>Тип заказа:</b><pre> Сайт</pre>\n'f'<b>Тип сайта:</b><pre> {data.get("lac")}</pre>\n'f'<b>Бюджет заказчика:</b><pre> {data.get("example")}</pre>\n'f'<b>Примеры сайтов:</b><pre> {data.get("name")}</pre>\n'f'<b>Техническое задание:</b> <pre>{data.get("money")}</pre>',
        reply_markup=inline(
            f"{message.chat.id}",
        ),
    )
    await state.finish()


@dp.callback_query_handler(reg_callback.filter(status="2"))
async def accept(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()

    await call.message.edit_reply_markup()

    nickname = call.data.split(":")[len(call.data.split(":")) - 1]

    accepting = f"<b>✅ Заказ был принят @{call.from_user.username} </b>\n\n " + call.message.text

    await bot.edit_message_text(
        chat_id = admin_chat_id, message_id = call.message.message_id, text = accepting
    )
    
    await bot.send_message(int(callback_data.get("chat_id")), f"<b>Ваш заказ был принят ✅</b>\nСейчас с вами свяжется разработчик @{call.from_user.username}. (Если вам не написали, пожалуйста напишите первым)")



@dp.message_handler(Text(equals="💎 Заказать дизайн"), state="*")
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        await state.update_data(name=message.text)
        await bot.send_message(
            message.chat.id, "<b>Укажите тип дизайна:</b>", reply_markup=design_tarif_keyboard
        )
        await Design.age.set()
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
        await Design.age.set()

@dp.message_handler(state=Design.age, content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        print (message)
        await state.update_data(money=message.text)
        await bot.send_message(
        message.chat.id, "<b>Укажите свой бюджет:</b>", reply_markup=cancel_keyboard
    )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
    await Design.lac.set()

@dp.message_handler(state=Design.lac, content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        print (message)
        await state.update_data(lac=message.text)
        await bot.send_message(
        message.chat.id, "<b>Опишите краткое техническое задание (Не прикрепляйте картинки):</b>", reply_markup=cancel_keyboard
    )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
    await Design.photo.set()

@dp.message_handler(state=Design.photo, content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    if message.from_user.username:
        print (message)
        await state.update_data(name=message.text)
        await bot.send_message(
        message.chat.id, "<b>Прикрепите примеры работ:</b>", reply_markup=cancel_keyboard
    )
    else:
        await bot.send_message(
            message.chat.id, "<b>Ошибка! Для продолжения вы должны поставить юзернейм.</b>", reply_markup=types.ReplyKeyboardRemove()
        )
    await Design.end.set()


@dp.message_handler(state=Design.end, content_types=types.ContentTypes.PHOTO)
async def confirmation(message: types.Message, state: FSMContext):
    await state.update_data(end=message.photo)
    data = await state.get_data()
    await bot.send_message(
        message.chat.id, "<b>Анкета успешно заполнена, после проверки вы получите ответ.</b>", reply_markup=reg_keyboard
    )
    
    await bot.send_photo(
        admin_chat_id,
        photo=message.photo[-1].file_id,
        caption=f"<b>💎 Новая заявка от </b>@{message.from_user.username}\n➖➖➖➖➖➖➖➖➖➖\n"f'<b>Тип заказа:</b><pre> Дизайн</pre>\n'f'<b>Тип дизайна:</b><pre> {data.get("money")}, {data.get("age")}</pre>\n'f'<b>Бюджет заказчика:</b> <pre>{data.get("lac")}</pre>\n'f'<b>Техническое задание:</b> <pre>{data.get("name")}</pre>',
        reply_markup=inline(
        f"{message.chat.id}",
        ),
    )
    await state.finish()


# Теперь пропишем хэндлеры для inline

@dp.callback_query_handler(reg_callback.filter(status="1"))
# callback данные мы сразу же приобразуем в словарь для удобства работы
async def decline(call: CallbackQuery, callback_data: dict):
    await call.answer()
    
    await bot.send_message(
        admin_chat_id, call.message.chat.id,  f"<b>❌ Заказ был отклонен @{call.from_user.username}, Причина: Нарушение правил проекта!</b>", reply_to_message_id=call.message.message_id
    )
    # Отправляем вердикт.
    await bot.send_message(int(callback_data.get("chat_id")), "<b>Ваш заказ был отклонен ❌</b>\nВозможно он нарушает политику проекта.")


@dp.callback_query_handler(reg_callback.filter(status="2"))
async def accept(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()

    await call.message.edit_reply_markup()

    nickname = call.data.split(":")[len(call.data.split(":")) - 1]

    accepting = f"<b>✅ Заказ был принят @{call.from_user.username} </b>\n\n " + call.message.caption

    await bot.edit_message_caption(
        chat_id = admin_chat_id, message_id = call.message.message_id, caption = accepting
    )
    # await bot.send_message(
    #         admin_chat_id, f"<b>🎉 Заказ был принят @{call.from_user.username}, свяжитесь с клиентом @{nickname}</b>", reply_to_message_id=call.message.message_id
    # )
    # Отправляем вердикт.
    await bot.send_message(int(callback_data.get("chat_id")), f"<b>Ваш заказ был принят ✅</b>\nСейчас с вами свяжется разработчик @{call.from_user.username}. (Если вам не написали, пожалуйста напишите первым)")



@dp.message_handler(commands=['listid'])
async def notify_users(message: types.Message):
    if message.from_id in admins_id: 
        for user in workers.find():
            await bot.send_message(message.chat.id, user['_id'])
    else: 
        await bot.send_message(message.chat.id, 'Вы не администратор!')


@dp.message_handler(commands=['stat'])
async def notify_users(message: types.Message):
    if message.from_id in admins_id: 
        users = workers.find()
        quantly = 0
        for user in users:
            quantly = quantly + 1

        await message.reply('Пользователей: ' + str(quantly))

    else: 
        await bot.send_message(message.chat.id, 'Вы не администратор!')

admins_id = [5557202913, 1511660386]

@dp.message_handler(commands=['sendall'])
async def notify_users(message: types.Message):
    if message.from_id in admins_id: 
        msg = message.text.replace('/sendall', '')
    
        for user in workers.find():
            try:
                await bot.send_message(user["_id"], msg)
            except:
                pass
    else: 
        await bot.send_message(message.chat.id, 'Вы не администратор!')

@dp.message_handler(commands=['мут', 'mute'], commands_prefix='./', is_chat_admin=True)
async def mute(message):
      name1 = message.from_user.get_mention(as_html=True)
      if not message.reply_to_message:
         await message.reply("Эта команда должна быть ответом на сообщение!")
         return
      try:
         muteint = int(message.text.split()[1])
         mutetype = message.text.split()[2]
         comment = " ".join(message.text.split()[3:])
      except IndexError:
         await message.reply('Не хватает аргументов!\nПример:\n`/мут 1 ч причина`')
         return
      if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
         dt = datetime.now() + timedelta(hours=muteint)
         timestamp = dt.timestamp()
         await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
         await message.reply(f'<b>Вы успешно замутили человека:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n\n<b>Причина:</b><pre> {comment}</pre>',  parse_mode='html')
      elif mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
         dt = datetime.now() + timedelta(minutes=muteint)
         timestamp = dt.timestamp()
         await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
         await message.reply(f'<b>Вы успешно замутили человека:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n\n<b>Причина:</b><pre> {comment}</pre>',  parse_mode='html')
      elif mutetype == "д" or mutetype == "дней" or mutetype == "день":
         dt = datetime.now() + timedelta(days=muteint)
         timestamp = dt.timestamp()
         await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
         await message.reply(f'<b>Вы успешно замутили человека:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n\n<b>Причина:</b><pre> {comment}</pre>',  parse_mode='html')

@dp.message_handler(commands=['бан', 'ban'], commands_prefix='./', is_chat_admin=True)
async def ban(message):
    if message.from_id in admins_id:
        reason = message.text.split()
        user_chat: types.Chat = await bot.get_chat(message.reply_to_message.from_user.id)
        await message.chat.kick(user_chat.id)
        await message.delete()
        await message.answer(f"Вы успешно заблокировали пользователя в чате!")
    else: 
        await bot.send_message(message.chat.id, 'Вы не администратор!')

if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)