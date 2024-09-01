from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, Float, ForeignKey, Boolean, JSON, BigInteger
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import text
import json

from utils import Skin

engine = create_engine("postgresql+psycopg2://root:root@localhost/pepe")
engine.connect()
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
db = SessionLocal()

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"

    ''' User Info '''
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    photo_id = Column(String)
    username = Column(String)
    join_first = Column(String, default = "None")
    join_last = Column(String, default = "None")
    level = Column(Integer, default = 1)
    
    ''' Balances Info '''
    views_balance = Column(BigInteger, default = 1000000)
    earn_balance = Column(BigInteger, default = 1000000)
    ton_balance = Column(Float, default = 0.00)

    ''' Daily Info '''
    daily_gifts = Column(String, default="None")
    daily_status = Column(Integer, default = 0)

    ''' Full Stamina '''
    full_stamina = Column(Integer, default = 3)
    full_stamina_last_date = Column(String, default = "None")
    
    ''' Referal '''
    invited_by = Column(BigInteger, default = 0)
    received_referal_gifts = Column(BigInteger, default = 0)

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'photo_id': self.photo_id,
            'username': self.username,
            'join_first': self.join_first,
            'join_last': self.join_last,
            'level': self.level,
            'balance': {
                'views': self.views_balance,
                'earn': self.earn_balance,
                'ton': self.ton_balance
            },
            'daily': {
                'gifts': self.daily_gifts,
                'status': self.daily_status
            },
            'full_stamina': self.full_stamina,
            'full_stamina_last_date': self.full_stamina_last_date,
            'invited_by': self.invited_by,
            'received_referal_gifts': self.received_referal_gifts
        }

class UserSettings(Base):
    __tablename__ = "user_settings"

    ''' User Settings '''
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String, default = "en")
    tap_animation = Column(Boolean, default = True)

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'language': self.language,
            'tap_animation': self.tap_animation
        }

class UserCosts(Base):
    __tablename__ = "user_costs"

    ''' User Costs '''
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    views_costs = Column(BigInteger, default = 30)
    money_costs = Column(BigInteger, default = 25)
    stamina_costs = Column(BigInteger, default = 150)
    ton_costs = Column(Float, default = 0.01)
    
    ''' User Costs Chances '''
    views_chance = Column(Float, default = 10)
    money_chance = Column(Float, default = 5)
    ton_chance = Column(Float, default = 0.12)
    
    ''' User Costs Auto-Chances '''
    auto_views_chance = Column(Float, default = 25)
    auto_money_chance = Column(Float, default = 25)
    auto_ton_chance = Column(Float, default = 0.00)
    
    ''' User Costs Profile '''
    profile_post_cost = Column(BigInteger, default = 250000)
    profile_afk_cost = Column(BigInteger, default = 200000)

    ''' User Costs Clicks '''
    stamina_now = Column(BigInteger, default = 150)

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'views_costs': self.views_costs,
            'money_costs': self.money_costs,
            'stamina_costs': self.stamina_costs,
            'ton_costs': self.ton_costs,
            'views_chance': self.views_chance,
            'money_chance': self.money_chance,
            'ton_chance': self.ton_chance,
            'auto_views_chance': self.auto_views_chance,
            'auto_money_chance': self.auto_money_chance,
            'auto_ton_chance': self.auto_ton_chance,
            'profile_post_cost': self.profile_post_cost,
            'profile_afk_cost': self.profile_afk_cost,
            'stamina_now': self.stamina_now
        }

class Invoices(Base):
    __tablename__ = "invoices"

    ''' Payments '''
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    invoice_id = Column(String)
    invoice_type = Column(String)
    invoice_amount = Column(BigInteger)
    invoice_status = Column(String)
    invoice_date = Column(String)

class Inventory(Base):
    __tablename__ = "inventory"

    ''' Inventory '''
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    item = Column(String)
    amount = Column(BigInteger)

class UserSkins(Base):
    __tablename__ = 'user_skins'
    
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    skin_id = Column(String)
    skin_category = Column(String)
    
    # rare
    skin_rare = Column(String)
    
    # одет/не одет
    skin_status = Column(Boolean)
    
    # показывать или нет
    skin_show = Column(Boolean)
    
    # характеристики скина
    skin_baffs = Column(JSON) 
    
    # настройки в магазине
    skin_shop = Column(JSON) 
    
    # настройки в апгрейдах
    skin_upgrade = Column(JSON)

    def as_dict(self) -> dict:
        name = None
        try:
            with open('./../names.json') as json_file:
                json_data = json.load(json_file)

            if json_data[self.skin_id]['name']:
                name = json_data[self.skin_id]['name']
                
        except Exception as e: 
            name = "None"


        return {
            'id': self.id,
            'user_id': self.user_id,
            'skin_id': self.skin_id,
            'skin_category': self.skin_category,
            'skin_rare': self.skin_rare,
            'skin_status': self.skin_status,
            'skin_show': self.skin_show,
            'skin_baffs': self.skin_baffs,
            'skin_shop': self.skin_shop,
            'skin_upgrade': self.skin_upgrade,
            'name': name,
            'clickable': Skin(self.skin_id).as_dict().get('clickable'),
            'z_index': Skin(self.skin_id).as_dict().get('z-index'),
            'profile_show': Skin(self.skin_id).as_dict().get('profile_show'),
        }
        

Base.metadata.create_all(bind = engine)

# def add_column(table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(dialect=engine.dialect)
#     alter_query = text(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')
#     db.execute(alter_query)
#     db.commit()

# skin_rare = Column("skin_rare", String, default = "rare")

# add_column("user_skins", skin_rare)

