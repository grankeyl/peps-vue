from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from config import cfg

if cfg.get("DEVELOPER_STATUS") == "True":
    domain = cfg.get("DOMAIN")
else:
    domain = cfg.get("DOMAIN_ORIG")

play_link = "{domain}/?user_id_js={user_id_js}"
test_play_link = "{domain}"

def start_menu(user_id_js):
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "EN Channel",
            url="https://t.me/PepsENG"
        ),
        InlineKeyboardButton(
            text = "RU Channel", 
            url="https://t.me/PepsRU"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "🐸 Play", 
            # web_app = WebAppInfo(url=play_link.format(domain=domain, user_id_js=user_id_js))
            web_app=WebAppInfo(url="https://whysk3a2bqy43cx36hqeh4ihyx6tk4uvq2ql7p6evtlmd7ombrvsx7v.adnl")
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def test_play_menu():
    markup = InlineKeyboardBuilder()
    
    markup.row(
        InlineKeyboardButton(
            text = "🐸 Play", 
            web_app = WebAppInfo(url=test_play_link.format(domain=domain))
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def play_menu(user_id_js):
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "🐸 Play", 
            web_app = WebAppInfo(url=play_link.format(domain=domain, user_id_js=user_id_js))
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def admin():
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "🔎 Поиск юзера",
            callback_data="admin:search"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "📊 Статистика",
            callback_data="admin:stat"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "📫 Рассылка",
            callback_data="admin:mail"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "⚙️ Настройки",
            callback_data="admin:settings"
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def admin_back():
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "‹ Назад",
            callback_data="admin_back:admin"
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def admin_exit():
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "‹ Отмена",
            callback_data="admin_back:exit"
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def admin_mail_photo():
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "💢 Без медиа",
            callback_data="mail_empty:photo"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "‹ Отмена",
            callback_data="admin_back:exit"
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def admin_mail_button():
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "💢 Без кнопки",
            callback_data="mail_empty:button_empty"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "✳️ Добавить кнопку",
            callback_data="mail_empty:button_add"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "‹ Отмена",
            callback_data="admin_back:exit"
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def button_mail(title, url):
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = f"{title}",
            url=url
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def mail_settings_send():
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "Рассылка в боте ›",
            callback_data="send_all"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "Рассылка в EN канал ›",
            callback_data="send_channels|en"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "Рассылка в RU канал ›",
            callback_data="send_channels|ru"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "‹ Отмена",
            callback_data="admin_back:exit"
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()

def admin_user_settings(user_id):
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text = "🧢 Подарить скин",
            callback_data=f"user_settings:gift_skin:{user_id}"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "💰 Подарить $PEPS",
            callback_data=f"user_settings:gift_money:{user_id}"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "👁 Подарить просмотры",
            callback_data=f"user_settings:gift_views:{user_id}"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text = "‹ Отмена",
            callback_data="admin_back:exit"
        )
    )
    
    markup.adjust(1)

    return markup.as_markup()