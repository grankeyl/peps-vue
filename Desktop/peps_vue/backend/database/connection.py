from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, Float, ForeignKey, Boolean, JSON, BigInteger
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import text, func

from datetime import datetime, timedelta
from utils import Skin, get_now_date, generate_referal_key, get_now_date_without_time

import json


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
    
    ''' Activity Info '''
    join_first = Column(String, default = get_now_date)
    join_last = Column(String, default = get_now_date)
    
    ''' Level Info '''
    experience = Column(Integer, default = 0)
    level = Column(Integer, default = 1)
    
    ''' Balances Info '''
    views_balance = Column(BigInteger, default = 100000)
    earn_balance = Column(BigInteger, default = 100000)
    ton_balance = Column(Float, default = 0.00)

    ''' Daily Info '''
    daily_gifts = Column(String, default = "")
    daily_status = Column(Boolean, default = False)
    daily_last_date = Column(String, default = " ")

    ''' Full Stamina '''
    full_stamina = Column(Integer, default = 3)
    full_stamina_last_date = Column(String, default = "None")
    
    ''' Referal '''
    referal_key = Column(String, default = generate_referal_key)
    invited_by = Column(String, default = "None")
    received_referal_gifts = Column(String, default = "None")
    
    ''' Tasks '''
    tasks_completed = Column(JSON, default = [])
    tasks_progress = Column(JSON, default = {})
    task_story = Column(Boolean, default = False)
    
    ''' Special '''
    special_completed = Column(JSON, default = [])

    def update_balance(self, type_amount: str, amount: str):
        amount_value = float(amount) if type_amount.lower() == 'ton' else int(amount)

        if type_amount.lower() in ['views', 'money', 'ton']:
            if amount.startswith('+'):
                if type_amount.lower() == 'views':
                    self.views_balance += amount_value
                elif type_amount.lower() == 'money':
                    self.earn_balance += amount_value
                elif type_amount.lower() == 'ton':
                    self.ton_balance += amount_value
            elif amount.startswith('-'):
                if type_amount.lower() == 'views':
                    self.views_balance -= amount_value
                elif type_amount.lower() == 'money':
                    self.earn_balance -= amount_value
                elif type_amount.lower() == 'ton':
                    self.ton_balance -= amount_value
            else:
                if type_amount.lower() == 'views':
                    self.views_balance = amount_value
                elif type_amount.lower() == 'money':
                    self.earn_balance = amount_value
                elif type_amount.lower() == 'ton':
                    self.ton_balance = amount_value

        db.flush()
        db.commit()

    ''' Метод для вычисления опыта на следующий уровень '''
    def required_xp_for_next_level(self):
        base_xp = 320
        multiplier = 1.1
        return int(base_xp * (self.level ** multiplier))
    
    ''' Метод для подсчета процентов на основе опыта '''
    def required_xp_for_percents(self):
        return (self.experience / self.required_xp_for_next_level()) * 100

    ''' Метод для добавления опыта '''
    def add_experience(self, xp_gained):
        self.experience += xp_gained

        ''' Проверяем, достаточно ли опыта для повышения уровня '''
        while self.experience >= self.required_xp_for_next_level():
            self.experience -= self.required_xp_for_next_level()
            self.level += 1

    @staticmethod
    def get_by_referal_key(referal_key: str):
        try:
            user = db.query(User).filter(User.referal_key == referal_key)

            if user.first():
                return user.first()
            else:
                return
        except:
            return

    @staticmethod
    def get_all_users():
        try:
            users = db.query(User).filter(User.username != 'Anonymous').all()
            user_dicts = [user.as_dict() for user in users]
            
            return user_dicts
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []

    @staticmethod
    def get_all_users_paid():
        try:
            users_paid = db.query(User).filter(User.username == 'Anonymous').all()
            user_dicts_paid = [user.as_dict() for user in users_paid]
            
            return user_dicts_paid
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
            
    @staticmethod
    def get_new_users_count():
        try:
            users = db.query(User).filter(User.join_first.startswith(get_now_date_without_time()), User.username != 'Anonymous').all()
            return len(users)
        except Exception as e:
            print(f"Error retrieving new users count: {e}")
            return 0

    @staticmethod
    def get_online_count():
        try:
            now = datetime.now()
            five_minutes_ago = now - timedelta(minutes=5)
            formatted_time = five_minutes_ago.strftime("%d-%m-%y %H:%M:%S")
            
            users = db.query(User).filter(User.join_last >= formatted_time, User.username != 'Anonymous').all()
            
            return len(users)
        except Exception as e:
            print(f"Error retrieving new users count: {e}")
            return 0
            
    @staticmethod
    def get_online_today_count():
        try:
            users = db.query(User).filter(User.join_last.startswith(get_now_date_without_time()), User.username != 'Anonymous').all()
            return len(users)
        except Exception as e:
            print(f"Error retrieving new users count: {e}")
            return 0

    @staticmethod
    def get_user(user_id):
        try:
            user_data = db.query(User).filter(User.user_id == user_id).first()
            return user_data.as_dict() if user_data else None
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def get_user_by_username(username):
        try:
            user_data = db.query(User).filter(User.username == username).first()
            return user_data.as_dict() if user_data else None
        except Exception as e:
            print(e)
            return None

    def as_dict(self) -> dict:

        referals = db.query(User).filter(User.invited_by == self.referal_key).all()
        
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
            'experience': self.experience,
            'experience_need': self.required_xp_for_next_level(),
            'experience_percent': self.required_xp_for_percents(),
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
            'referal_key': self.referal_key,
            'invited_by': self.invited_by,
            'received_referal_gifts': self.received_referal_gifts,
            'tasks_completed': self.tasks_completed,
            'tasks_progress': self.tasks_progress,
            'task_story': self.task_story,
            'special_completed': self.special_completed,
            'referals': len(referals)
        }

class UserSettings(Base):
    __tablename__ = "user_settings"

    ''' User Settings '''
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String, default = "en")
    tap_animation = Column(Boolean, default = True)

    @staticmethod
    def get_user(user_id):
        try:
            user_data = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
            return user_data.as_dict() if user_data else None
        except Exception as e:
            print(e)
            return None

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
    ton_chance = Column(Float, default = 1.35)
    
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

        equipment_items = [
            'systembox', 'monitors', 'keyboard',
            'mouse', 'chair', 'table'
        ]
        
        profile_baffs = {'views_costs': self.views_costs, 'money_costs': self.money_costs, 'stamina_costs': self.stamina_costs}
        puton_skins = UserSkins.get_puton_skins(self.user_id)

        for skin in puton_skins:
            skin_without_id = str(skin['skin_id']).split('_')[0]
            if skin['skin_baffs']['baffs_type'] is True:
                if str(skin_without_id).lower() in equipment_items:
                    skin = db.query(UserSkins).filter(UserSkins.user_id == self.user_id, UserSkins.skin_id == skin_without_id + "_0").first().as_dict()

                if str(skin_without_id).lower() in equipment_items:
                    if int(skin['skin_upgrade']['upgrades_level_step']) == 1 and int(skin['skin_upgrade']['upgrades_level']) == 1:
                        continue

                if skin['skin_baffs']['baffs_buy_type'] == "money":
                    profile_baffs['money_costs'] = profile_baffs['money_costs'] + skin['skin_baffs']['baffs_adding_money']
                elif skin['skin_baffs']['baffs_buy_type'] == "views":
                    profile_baffs['views_costs'] = profile_baffs['views_costs'] + skin['skin_baffs']['baffs_adding_views']
                elif skin['skin_baffs']['baffs_buy_type'] == "stamina":
                    profile_baffs['stamina_costs'] = profile_baffs['stamina_costs'] + skin['skin_baffs']['baffs_adding_stamina']

        return {
            'id': self.id,
            'user_id': self.user_id,
            'views_costs': int(profile_baffs['views_costs']),
            'money_costs': int(profile_baffs['money_costs']),
            'stamina_costs': int(profile_baffs['stamina_costs']),
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
    invoice_params = Column(JSON)
    invoice_amount = Column(BigInteger)
    invoice_status = Column(String)
    invoice_date = Column(String, default = get_now_date())

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'invoice_id': self.invoice_id,
            'invoice_params': self.invoice_params,
            'invoice_amount': self.invoice_amount,
            'invoice_status': self.invoice_status,
            'invoice_date': self.invoice_date
        }

    @staticmethod
    def is_exist(invoice_id: str) -> bool:
        if db.query(Invoices).filter(Invoices.invoice_id == invoice_id).first():
            return True

        return False

    @staticmethod
    def get_total_invoice_amount():
        try:
            total_amount = db.query(func.sum(Invoices.invoice_amount)).filter(Invoices.invoice_status == 'paid').scalar()
            return total_amount if total_amount else 0
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_total_invoice_today_amount():
        try:
            total_amount = db.query(func.sum(Invoices.invoice_amount)).filter(Invoices.invoice_status == 'paid', Invoices.invoice_date.startswith(get_now_date_without_time())).scalar()
            return total_amount if total_amount else 0
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_total_invoice_amount_user(user_id):
        try:
            total_amount = db.query(func.sum(Invoices.invoice_amount)).filter(Invoices.invoice_status == 'paid', Invoices.user_id == user_id).scalar()
            return total_amount if total_amount else 0
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_total_invoice_today_amount_user(user_id):
        try:
            total_amount = db.query(func.sum(Invoices.invoice_amount)).filter(Invoices.invoice_status == 'paid', Invoices.invoice_date.startswith(get_now_date_without_time()), Invoices.user_id == user_id).scalar()
            return total_amount if total_amount else 0
        except Exception as e:
            print(e)
            return None

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

    @staticmethod
    def get_puton_skins(user_id: int):
        skins = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_status == True).all()
        return [x.as_dict() for x in skins]

    @staticmethod
    def get_quantity_count(skin_id: int):
        skins = db.query(UserSkins).filter(UserSkins.skin_id == skin_id).all()
        return len(skins)

    def as_dict(self) -> dict:
        name = None
        description = None
        description_ru = None
        try:
            with open('./../names.json', 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)

            if json_data[self.skin_id]['name']:
                name = json_data[self.skin_id]['name']
                description = json_data[self.skin_id]['description']
                description_ru = json_data[self.skin_id]['description_ru']
                
        except Exception as e: 
            name = "None"
            description = "None"
            description_ru = "None"

        return {
            'id': self.id,
            'user_id': self.user_id,
            'skin_id': self.skin_id,
            'skin_take': Skin(self.skin_id).as_dict().get('take'),
            'skin_quantity_need': Skin(self.skin_id).as_dict().get('quantity'),
            'skin_quantity_count': self.get_quantity_count(self.skin_id),
            'skin_category': self.skin_category,
            'skin_rare': self.skin_rare,
            'skin_status': self.skin_status,
            'skin_show': self.skin_show,
            'skin_baffs': self.skin_baffs,
            'skin_shop': self.skin_shop,
            'skin_upgrade': self.skin_upgrade,
            'name': name,
            'description': description,
            'description_ru': description_ru,
            'clickable': Skin(self.skin_id).as_dict().get('clickable'),
            'z_index': Skin(self.skin_id).as_dict().get('z-index'),
            'profile_show': Skin(self.skin_id).as_dict().get('profile_show'),
        }

    @staticmethod
    def get_baffs(user_id: int) -> dict:
        skins = db.query(UserSkins).filter(UserSkins.skin_status == True, UserSkins.user_id == user_id).all()
        
        baffs = {'views': 0, 'money': 0, 'stamina': 0}

        equipment_items = [
            'systembox', 'monitors', 'keyboard',
            'mouse', 'chair', 'table'
        ]

        for skin in skins:
            skin_without_number = skin.skin_id.split('_')[0]
            if skin_without_number in equipment_items:
                skin_id = skin_without_number + "_0"
            else:
                skin_id = skin.skin_id

            data_skin = db.query(UserSkins).filter(UserSkins.skin_id == skin_id, UserSkins.user_id == user_id).first().as_dict()

            if isinstance(data_skin['skin_baffs'], dict) and data_skin['skin_baffs'].get('baffs_type') is True:
                baffs['views'] += int(data_skin['skin_baffs'].get('baffs_adding_views', 0))
                baffs['money'] += int(data_skin['skin_baffs'].get('baffs_adding_money', 0))
                baffs['stamina'] += int(data_skin['skin_baffs'].get('baffs_adding_stamina', 0))
                
        return baffs

    def skin_list(self) -> list[dict]:
        skins = db.query(UserSkins).filter(UserSkins.user_id == self.user_id).all()
        return [skin.skin_id for skin in skins]

    def get_skin(user_id: int, skin_id: str):
        skins = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_id == skin_id).first()
        return skins.as_dict() if skins else None
        

class Tasks(Base):
    __tablename__ = 'tasks'
    
    id = Column(BigInteger, primary_key=True)
    task_name = Column(String)
    task_name_ru = Column(String)
    task_type = Column(String)
    task_steps = Column(Integer, default = 1)
    task_photo = Column(String)
    task_status = Column(Boolean, default = True)
    task_created = Column(String, default = get_now_date())
    task_redirect = Column(String)
    task_gift_type = Column(String)
    task_gift = Column(Integer)

    def as_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_name_ru': self.task_name_ru,
            'task_type': self.task_type,
            'task_photo': self.task_photo,
            'task_status': self.task_status,
            'task_created': self.task_created,
            'task_redirect': self.task_redirect,
            'task_gift_type': str(self.task_gift_type).lower(),
            'task_gift': self.task_gift,
            'task_steps': self.task_steps
        }

    def get_current_progress(self, user_id: int) -> dict:
        user = db.query(User).filter(User.user_id == user_id).first()

        if isinstance(user.tasks_progress, str):
            current_progress = json.loads(user.tasks_progress)
        else:
            current_progress = user.tasks_progress

        return current_progress[str(self.id)]



    @staticmethod
    def get_tasks(user_id: int = None) -> list[dict]:
        tasks = db.query(Tasks).filter(Tasks.task_status == True).all()
        
        tasks_result = []
        completed_tasks = []
        user = None

        if user_id:
            user = db.query(User).filter(User.user_id == user_id).first()
            
            if user:
                completed_tasks = user.tasks_completed
                tasks_result.append({ 'id': "story", "completed": user.task_story, 'task_progress': {} })
    
        if not user_id:
            return [x.as_dict() for x in tasks]

        if tasks:
            for task in tasks:
                dict_task = task.as_dict()
                
                if int(dict_task['id']) in completed_tasks:
                    dict_task['completed'] = True
                else:
                    dict_task['completed'] = False
                
                if user:
                    if user.tasks_progress and user.tasks_progress != {}:
                        task_progress = user.tasks_progress.get(str(dict_task['id']), False)
                        dict_task['task_progress'] = task_progress
                    else:
                        dict_task['task_progress'] = False
                else:
                    dict_task['task_progress'] = False

                tasks_result.append(dict_task)

        return list(tasks_result)

    def start_task(self, user_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if isinstance(user.tasks_progress, str):
            current_progress = json.loads(user.tasks_progress)
        else:
            current_progress = user.tasks_progress

        current_progress = dict(current_progress)

        if str(self.id) not in current_progress.keys():
            current_progress[str(self.id)] = {'steps': self.task_steps, 'current_step': 0}
            user.tasks_progress = current_progress
            
        db.flush()
        db.commit()

    def next_step(self, user_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()

        if isinstance(user.tasks_progress, str):
            current_progress = json.loads(user.tasks_progress)
        else:
            current_progress = user.tasks_progress

        current_step = int(current_progress[str(self.id)]['current_step'])
        current_progress[str(self.id)]['current_step'] = current_step + 1

        update_query = text("""
            UPDATE users
            SET tasks_progress = :tasks_progress
            WHERE user_id = :user_id
        """)
        db.execute(update_query, {
            'tasks_progress': json.dumps(current_progress),
            'user_id': user_id
        })

        db.commit()

        updated_user = db.query(User).filter(User.user_id == user_id).first()

        if current_progress[str(self.id)]['current_step'] >= current_progress[str(self.id)]['steps']:
            return True
        else:
            return updated_user.tasks_progress

    def end_task(self, user_id: int, views: int, earn: int, ton: float):
        user = db.query(User).filter(User.user_id == user_id).first()
        completed_tasks = user.tasks_completed
        
        user.views_balance = int(views)
        user.earn_balance = int(earn)
        user.ton_balance = float(ton)
        
        if self.id in completed_tasks:
            pass
        else:
            user.tasks_completed.append(self.id)

            update_query = text("""
                UPDATE users
                SET tasks_completed = :tasks_completed
                WHERE user_id = :user_id
            """)
            db.execute(update_query, {
                'tasks_completed': json.dumps(user.tasks_completed),
                'user_id': user_id
            })

        db.commit()

    @staticmethod
    def clear():
        db.query(Tasks).delete()
        db.commit()
        db.execute(text("ALTER SEQUENCE tasks_id_seq RESTART WITH 1"))
        db.commit()

class Daily(Base):
    __tablename__ = "daily"

    ''' Daily gifts '''
    id = Column(BigInteger, primary_key=True)
    gift_uuid = Column(Integer)
    gift_type = Column(String)
    gift_amount = Column(String)
    gift_skin = Column(String)
    gift_created = Column(String, default = get_now_date())
    gift_status = Column(Boolean, default = True)
    
    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'gift_uuid': self.gift_uuid,
            'gift_type': self.gift_type,
            'gift_amount': self.gift_amount,
            'gift_skin': self.gift_skin,
            'gift_created': self.gift_created,
            'gift_status': self.gift_status,
        }
        
    @staticmethod
    def get_daily_all() -> list[dict]:
        daily_gifts = db.query(Daily).all()
        gifts = []

        for gift in daily_gifts:
            gift_data = gift.as_dict()
            if str(gift_data['gift_type']).lower() == "skin":
                skin = Skin(gift_data['gift_skin']).as_dict()
                
                gift_data['rare'] = skin.get('rare')
                gift_data['baffs_percentage'] = skin.get('baffs').get('baffs_buy_percentage')
                gift_data['baffs_type'] = skin.get('baffs').get('baffs_type')
                gift_data["baffs_buy_type"] = skin.get('baffs').get('baffs_buy_type')

            gifts.append(gift_data)
            
        return list(gifts)

    @staticmethod
    def clear():
        db.query(Daily).delete()
        db.commit()
        db.execute(text("ALTER SEQUENCE daily_id_seq RESTART WITH 1"))
        db.commit()

class UserBank(Base):
    __tablename__ = "user_bank"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    views = Column(Integer)
    earn = Column(Integer)
    ton = Column(Float)
    stamina = Column(Integer)

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'views': int(self.views),
            'earn': int(self.earn),
            'ton': float(self.ton),
            'stamina': int(self.stamina)
        }

    def clear(self):
        if self.views != 0:
            self.views = 0
        if self.earn != 0:
            self.earn = 0
        if self.ton != 0:
            self.ton = 0
        if self.stamina != 0:
            self.stamina = 0

    @staticmethod
    def get_by_user(user: User):
        bank = db.query(UserBank).filter(UserBank.user_id == user.user_id).first()

        if bank:
            return bank
        else:
            db.add(UserBank(
                user_id = user.user_id,
                earn = 0,
                views = 0,
                stamina = 0,
                ton = 0
            ))
            
            db.flush()
            db.commit()
            
            bank = db.query(UserBank).filter(UserBank.user_id == user.user_id).first()
            return bank
        
Base.metadata.create_all(bind = engine)

# def add_column(table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(dialect=engine.dialect)
#     alter_query = text(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')
#     db.execute(alter_query)
#     db.commit()

# skin_rare = Column("skin_rare", String, default = "rare")

# add_column("user_skins", skin_rare)
