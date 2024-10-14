from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from config import cfg

from sqlalchemy import text, func
from database.connection import db, User, UserSettings, UserCosts, UserSkins, UserBank
from utils import get_now_date, get_now_date_without_time

from utils import Skin
from datetime import datetime

import json
import random

router_user = APIRouter()
router_key = "{}/user".format(cfg.get("ROUTER_KEY"))

@router_user.get('{}/create'.format(router_key))
async def user_create(request: Request):
    '''
    Create User in Database
    '''
    # try:
    data = dict(request.query_params)

    secret_key = data.get('key')
    user_id = data.get('user_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    full_name = data.get('full_name')
    username = data.get('username')
    photo_id = data.get('photo_id')
    invited_by = data.get('invited_by')
    
    existing_user = None

    if secret_key == cfg.get('SECRET_KEY'):
        try:
            existing_user = db.query(User).filter(User.user_id == int(user_id)).first()
        except Exception as E:
            print(E)
        
        if existing_user:
            return JSONResponse({ 'success': False, 'error': 'exists' })

        user = User(
            user_id = user_id,
            first_name = first_name,
            last_name = last_name,
            full_name = full_name,
            username = username,
            photo_id = photo_id,
            invited_by = invited_by,
            join_first = get_now_date()
        )
        db.add(user)

        db.add(UserSettings(
            user_id = user_id
        ))

        db.add(UserCosts(
            user_id = user_id
        ))
        
        db.flush()
        db.commit()


        with open('./constants.json', 'r', encoding='utf-8') as json_file:
            constants = json.load(json_file)

        for skin_id in constants['default_skins']:
            skin = Skin(skin_id)
            data_skin = skin.as_dict()
            category_data = skin.category_dict()
                        
            user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()
            
            if data_skin['baffs']['baffs_type'] is True:
                
                if data_skin['baffs']['baffs_buy_type'] == 'views':
                    data_skin['baffs']['baffs_adding_views'] = (user_costs.views_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                    
                elif data_skin['baffs']['baffs_buy_type'] == 'money':
                    data_skin['baffs']['baffs_adding_money'] = (user_costs.money_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                    
                elif data_skin['baffs']['baffs_buy_type'] == 'stamina':
                    data_skin['baffs']['baffs_adding_stamina'] = (user_costs.stamina_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                
                elif data_skin['baffs']['baffs_buy_type'] == 'ton':
                    user_costs.ton_chance = user_costs.ton_chance + (user_costs.ton_chance / 100 * data_skin['baffs']['baffs_buy_percentage'])
            
            db.add(UserSkins(
                user_id = user_id,
                skin_id = skin_id,
                skin_category = skin.category,
                skin_rare = data_skin['rare'],
                skin_status = True,
                skin_show = category_data['skin_show'],
                skin_baffs = data_skin['baffs'],
                skin_shop = data_skin['shop_settings'],
                skin_upgrade = data_skin['upgrades_settings']
            ))

        # REFERAL SYSTEM
        if str(invited_by).lower() != 'none':
            invited_by_user = User.get_by_referal_key(invited_by)
            
            if invited_by_user:
                invited_by_user_bank = UserBank.get_by_user(invited_by_user)
                skin = Skin("item-table_0")
                data_skin = skin.as_dict()
                category_data = skin.category_dict()
                        
                user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()
                
                if data_skin['baffs']['baffs_type'] is True:
                    
                    if data_skin['baffs']['baffs_buy_type'] == 'views':
                        data_skin['baffs']['baffs_adding_views'] = (user_costs.views_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                    elif data_skin['baffs']['baffs_buy_type'] == 'money':
                        data_skin['baffs']['baffs_adding_money'] = (user_costs.money_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                    elif data_skin['baffs']['baffs_buy_type'] == 'stamina':
                        data_skin['baffs']['baffs_adding_stamina'] = (user_costs.stamina_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                    
                    elif data_skin['baffs']['baffs_buy_type'] == 'ton':
                        user_costs.ton_chance = user_costs.ton_chance + (user_costs.ton_chance / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                _dataSkin = UserSkins.get_skin(invited_by_user.user_id, "item-table_0")
                                        
                if _dataSkin is None:
                    db.add(UserSkins(
                        user_id = invited_by_user.user_id,
                        skin_id = "item-table_0",
                        skin_category = skin.category,
                        skin_rare = data_skin['rare'],
                        skin_status = True,
                        skin_show = category_data['skin_show'],
                        skin_baffs = data_skin['baffs'],
                        skin_shop = data_skin['shop_settings'],
                        skin_upgrade = data_skin['upgrades_settings']
                    ))

                    invited_by_user.received_referal_gifts = str("|".join([get_now_date(), "item-table_0"]))
                    invited_by_user_bank.earn = invited_by_user_bank.earn + 2500

                # invited_by_user.earn_balance = int(invited_by_user.earn_balance) + 2500

                new_balance_referal = user.earn_balance + 2500
                user.earn_balance = new_balance_referal

                skin = Skin("cap_3")
                data_skin = skin.as_dict()
                category_data = skin.category_dict()
                        
                user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()
                
                if data_skin['baffs']['baffs_type'] is True:
                    
                    if data_skin['baffs']['baffs_buy_type'] == 'views':
                        data_skin['baffs']['baffs_adding_views'] = (user_costs.views_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                    elif data_skin['baffs']['baffs_buy_type'] == 'money':
                        data_skin['baffs']['baffs_adding_money'] = (user_costs.money_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                    elif data_skin['baffs']['baffs_buy_type'] == 'stamina':
                        data_skin['baffs']['baffs_adding_stamina'] = (user_costs.stamina_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                    
                    elif data_skin['baffs']['baffs_buy_type'] == 'ton':
                        user_costs.ton_chance = user_costs.ton_chance + (user_costs.ton_chance / 100 * data_skin['baffs']['baffs_buy_percentage'])

                db.add(UserSkins(
                    user_id = user.user_id,
                    skin_id = "cap_3",
                    skin_category = skin.category,
                    skin_rare = data_skin['rare'],
                    skin_status = True,
                    skin_show = category_data['skin_show'],
                    skin_baffs = data_skin['baffs'],
                    skin_shop = data_skin['shop_settings'],
                    skin_upgrade = data_skin['upgrades_settings']
                ))

        db.flush()
        db.commit()

        return JSONResponse({ 'success': True, 'data': { 'user_id': user_id } })
    else:
        return JSONResponse({ 'success': False, 'error': 'wrong key' })
    
    # except Exception as e:
    #     db.rollback()
    #     print(e, 123424)
    #     return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/get'.format(router_key))
async def user_get(request: Request):
    '''
    Get User in Database
    '''
    try:
        secret_key = dict(request.query_params).get('key')
        user_id_str = dict(request.query_params).get('user_id')
        user_id = int(user_id_str)

        if secret_key == cfg.get('SECRET_KEY'):
            user_data = db.query(User).filter(User.user_id == user_id).first()
                
            user_settings_data = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
            user_costs_data = db.query(UserCosts).filter(UserCosts.user_id == user_id).first().as_dict()

            return JSONResponse({
                'success': True,
                'data': {
                    'user': dict(user_data.as_dict()) if user_data else {},
                    'settings': dict(user_settings_data.as_dict()) if user_settings_data else {},
                    'costs': dict(user_costs_data) if user_costs_data else {}
                }
            })
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })

    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({ 'success': False, 'error': str(e) })


@router_user.get('{}/updateGame'.format(router_key))
async def update_game(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        views = dict(request.query_params).get('views')
        earn = dict(request.query_params).get('earn')
        ton = dict(request.query_params).get('ton')
        stamina = dict(request.query_params).get('stamina')
        experience = dict(request.query_params).get('experience')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()
            
            user.add_experience(int(experience))

            if user and user_costs:
                user_bank = UserBank.get_by_user(user)

                user.views_balance = int(views) + user_bank.views
                user.earn_balance = int(earn) + user_bank.earn
                user.ton_balance = float(ton) + user_bank.ton
            
                user_costs.stamina_now = int(stamina)

                user_bank.clear()

                db.flush()
                db.commit()
            else:
                return JSONResponse({ 'success': False, 'error': "user not exsist" })

            return JSONResponse({'success': True, 'balances': {'earn': user.earn_balance, 'views': user.views_balance, 'ton': user.ton_balance}})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
        
    except Exception as e:
        db.rollback()
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/get/full_stamina'.format(router_key))
async def get_full_stamina(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()

            if user:
                if user.full_stamina != 0:
                    if not user.full_stamina:
                        user.full_stamina = 3

                    user_costs.stamina_now = user_costs.stamina_costs
                    user.full_stamina = int(user.full_stamina) - 1
                    user.full_stamina_last_date = get_now_date()
                    
                    db.flush()
                    db.commit()

                    return JSONResponse({ 'success': True, 'data': user_costs.stamina_costs })

                else:
                    return JSONResponse({ 'success': False, 'error': 'not enough' })
            else:
                return JSONResponse({ 'success': False, 'error': 'user is not founded' })
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })

    except Exception as e:
        db.rollback()
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/update/full_stamina'.format(router_key))
async def update_full_stamina(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()

            if user:
                user.full_stamina = 3
                user.full_stamina_last_date = "None"
                
                db.flush()
                db.commit()

                return JSONResponse({ 'success': True, 'data': user.full_stamina })
            else:
                return JSONResponse({ 'success': False, 'error': 'user is not founded' })
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
            
    except Exception as e:
        db.rollback()
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/update/buy'.format(router_key))
async def update_buy(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        type = dict(request.query_params).get('type')
        amount = dict(request.query_params).get('amount')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            
            if type == "views":
                user.views_balance = int(user.views_balance) - int(amount)
                
                if float(user.views_balance) <= 0:
                    new_balance = 0
                else:
                    new_balance = user.views_balance
                
                user.views_balance = new_balance
                
            elif type == "money":
                user.earn_balance = int(user.earn_balance) - int(amount)
                
                if float(user.earn_balance) <= 0: 
                    new_balance = 0
                else: 
                    new_balance = user.earn_balance
                    
                user.earn_balance = new_balance
                
            elif type == "stars":
                print("###################")
                new_balance = 0
                
            else:
                user.ton_balance = float(user.ton_balance) - float(amount)
                
                if float(user.ton_balance) <= 0: 
                    new_balance = 0
                else: 
                    new_balance = user.ton_balance
                    
                user.ton_balance = new_balance

            db.flush()
            db.commit()
        
            return JSONResponse({'success': True, 'balance': new_balance})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
        
    except Exception as e:
        db.rollback()
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/update/post_chances'.format(router_key))
async def update_post_chances(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        views_chance = dict(request.query_params).get('view_chance')
        money_chance = dict(request.query_params).get('money_chance')
        new_cost = dict(request.query_params).get('new_cost')
        
        type = None

        if secret_key == cfg.get('SECRET_KEY'):
            try:
                type = dict(request.query_params).get('type')
            except:
                type = "default"

            costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()

            if type.lower() == 'default':
                costs.views_chance = views_chance
                costs.money_chance = money_chance
                costs.profile_post_cost = new_cost

            elif type.lower() == 'afk':
                costs.auto_views_chance = views_chance
                costs.auto_money_chance = money_chance
                costs.profile_afk_cost = new_cost

            else:
                return JSONResponse({'success': False, 'error': 'not supported type'})

            db.flush()
            db.commit()

            return JSONResponse({'success': True, 'views_chance': int(views_chance), 'money_chance': int(money_chance)})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })

    except Exception as e:
        db.rollback()
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/update/settings'.format(router_key))
async def update_settings(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        language = dict(request.query_params).get('language')
        tap_animation = dict(request.query_params).get('tap_animation')
        new_tap_animation = False

        if secret_key == cfg.get('SECRET_KEY'):
            settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()

            if str(tap_animation).lower() == 'false': new_tap_animation = False
            else: new_tap_animation = True
            
            settings.tap_animation = new_tap_animation
            settings.language = str(language)

            db.flush()
            db.commit()

            return JSONResponse({'success': True, 'settings': {'language': language, 'tap_animation': tap_animation}})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
    
    except Exception as e:
        db.rollback()
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/getSkins'.format(router_key))
async def get_skins(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')

        if secret_key == cfg.get('SECRET_KEY'):
            skins = db.query(UserSkins).filter(UserSkins.user_id == user_id).all()

            skins_list = []

            with open('../categoriesArray.json', 'r', encoding='utf-8') as json_file:
                categories = json.load(json_file)

            for skin in skins:
                skins_list.append(skin.as_dict())

            return JSONResponse({'success': True, 'skins': skins_list, 'categories': [x[0].upper() + x[1:] for x in categories]})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
        
    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/getPutonSkins'.format(router_key))
async def get_puton_skins(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')

        if secret_key == cfg.get('SECRET_KEY'):
            skins = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_status == True).all()

            return JSONResponse({'success': True, 'skins': [skin.as_dict() for skin in skins], 'skins_list': [skin.as_dict()['skin_id'] for skin in skins]})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
        
    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/upgradeSkin'.format(router_key))
async def upgrade_skin(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        skin_id = dict(request.query_params).get('skin_id')
        upgrade = dict(request.query_params).get('upgrade')
        baffs = dict(request.query_params).get('baffs')
        
        if secret_key == cfg.get('SECRET_KEY'):
            if isinstance(upgrade, str):
                upgrade = json.loads(upgrade)
                baffs = json.loads(baffs)

            skin = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_id == skin_id).first()
            user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()
            
            if skin:
                skin.skin_upgrade = upgrade
                skin.skin_baffs = baffs
                
                if baffs['baffs_type'] is True:
                    if baffs['baffs_buy_type'] == 'ton':
                        user_costs.ton_chance = user_costs.ton_chance + (user_costs.ton_chance / 100 * baffs['baffs_buy_percentage'])
                
            else:
                return JSONResponse({'success': False, 'error': 'not founded skin'})

            db.flush()
            db.commit()

            return JSONResponse({'success': True, 'upgrade': upgrade})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })

    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/buySkin'.format(router_key))
async def buy_skin(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        skin_id = dict(request.query_params).get('skin_id')

        if secret_key == cfg.get('SECRET_KEY'):
            skin = Skin(skin_id)
            data_skin = skin.as_dict()
            category_data = skin.category_dict()
            
            exists_skin = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_id == skin_id).first()
            user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()

            if not exists_skin:
                
                if data_skin['baffs']['baffs_type'] is True:
                    
                    if data_skin['baffs']['baffs_buy_type'] == 'views':
                        data_skin['baffs']['baffs_adding_views'] = (user_costs.views_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                    elif data_skin['baffs']['baffs_buy_type'] == 'money':
                        data_skin['baffs']['baffs_adding_money'] = (user_costs.money_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                    elif data_skin['baffs']['baffs_buy_type'] == 'stamina':
                        data_skin['baffs']['baffs_adding_stamina'] = (user_costs.stamina_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                    
                    elif data_skin['baffs']['baffs_buy_type'] == 'ton':
                        user_costs.ton_chance = user_costs.ton_chance + (user_costs.ton_chance / 100 * data_skin['baffs']['baffs_buy_percentage'])
                
                db.add(UserSkins(
                    user_id = user_id,
                    skin_id = skin_id,
                    skin_category = skin.category,
                    skin_rare = data_skin['rare'],
                    skin_status = True,
                    skin_show = category_data['skin_show'],
                    skin_baffs = data_skin['baffs'],
                    skin_shop = data_skin['shop_settings'],
                    skin_upgrade = data_skin['upgrades_settings']
                ))

            db.flush()
            db.commit()

            return JSONResponse({'success': True, 'skin': skin_id})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })

    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})


@router_user.get('{}/skinChange'.format(router_key))
async def change_skin(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        skin_id = dict(request.query_params).get('skin_id')

        if secret_key == cfg.get('SECRET_KEY'):
            change_skin_data = await changeSkinFunc(user_id, skin_id)
            # return change_skin_data
            
            change_skin_data['costs'] = db.query(UserCosts).filter(UserCosts.user_id == user_id).first().as_dict()

            return change_skin_data

    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})


@router_user.get('{}/unPutSkin'.format(router_key))
async def un_put_skin(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        skin_id = dict(request.query_params).get('skin_id')

        if secret_key == cfg.get('SECRET_KEY'):
            skin = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_id == skin_id).first()
            
            if bool(skin.as_dict()['skin_take']):
                skin.skin_status = False
                
                db.flush()
                db.commit()
            else:
                return JSONResponse({'success': False})

            return JSONResponse({'success': True, 'costs': db.query(UserCosts).filter(UserCosts.user_id == user_id).first().as_dict()})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })

    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})


@router_user.get('{}/update/balance'.format(router_key))
async def update_balance(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        
        type_amount = dict(request.query_params).get('type')
        amount = dict(request.query_params).get('amount')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            
            if type_amount.lower() == 'views':
                if amount.startswith('+'):
                    user.views_balance = int(user.views_balance) + int(amount)
                elif amount.startswith('-'):
                    user.views_balance = int(user.views_balance) - int(amount)
                else:
                    user.views_balance = int(amount)
                    
            elif type_amount.lower() == 'money':
                if amount.startswith('+'):
                    user.earn_balance = int(user.earn_balance) + int(amount)
                elif amount.startswith('-'):
                    user.earn_balance = int(user.earn_balance) - int(amount)
                else:
                    user.earn_balance = int(amount)
            
            if type_amount.lower() == 'ton':
                if amount.startswith('+'):
                    user.ton_balance = float(user.ton_balance) + float(amount)
                elif amount.startswith('-'):
                    user.ton_balance = float(user.ton_balance) - float(amount)
                else:
                    user.ton_balance = float(amount)

            db.flush()
            db.commit()
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })

    except Exception as e:
        db.rollback()
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/get_referals'.format(router_key))
async def get_referals(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            
            if user:
                referals = (
                    db.query(User)
                    .filter(User.invited_by == user.referal_key)
                    .order_by(func.to_timestamp(User.join_first, 'DD-MM-YY HH24:MI:SS').desc())
                    .all()
                )
                return JSONResponse({'success': True, 'referals': [x.as_dict() for x in referals]})
            else:
                return JSONResponse({'success': False})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
            
    except Exception as e:
        db.rollback()
        return JSONResponse({'success': False, 'error': str(e)})


@router_user.get('{}/addExperience'.format(router_key))
async def add_experience_backend(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        experience = dict(request.query_params).get('experience')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            user.add_experience(int(experience))
            
            return JSONResponse({'success': True})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
        
    except Exception as e:
        db.rollback()
        return JSONResponse({ 'success': False, 'error': str(e) })
    
@router_user.get('{}/afkStamina'.format(router_key))
async def afk_stamina(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()

            if user and user_costs:
                last_date = user.join_last
                old_stamina = user_costs.stamina_now
                new_date = get_now_date()
                date_format = "%d-%m-%y %H:%M:%S"
                
                last_datetime = datetime.strptime(last_date, date_format)
                new_datetime = datetime.strptime(new_date, date_format)
                delta = new_datetime - last_datetime
                delta_seconds = delta.total_seconds()
                stamina_gained = int(delta_seconds // 5)

                stamina_gained = min(user_costs.stamina_now + stamina_gained, user_costs.stamina_costs)

                user_costs.stamina_now = stamina_gained
                user.join_last = new_date
                
                db.flush()
                db.commit()

                return JSONResponse({'success': True, 'old_stamina': old_stamina, 'new_stamina': user_costs.stamina_now})
            else:
                return JSONResponse({'success': False})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
            
    except Exception as e:
        db.rollback()
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/updateSpecials'.format(router_key))
async def update_specials(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        special_id = dict(request.query_params).get('special_id')

        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            
            if user:
                user.special_completed.append(special_id)

                update_query = text("""
                    UPDATE users
                    SET special_completed = :special_completed
                    WHERE user_id = :user_id
                """)
                db.execute(update_query, {
                    'special_completed': json.dumps(user.special_completed),
                    'user_id': user_id
                })
            
                db.flush()
                db.commit()

                return JSONResponse({'success': True, 'data': user.special_completed})
            else:
                return JSONResponse({'success': False})
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
        
    except Exception as e:
        db.rollback()
        return JSONResponse({'success': False, 'error': str(e)})
    
async def changeSkinFunc(user_id: int, skin_id: str):
    skin_without_id = skin_id.split('_')[0]
    
    put_on_skins = db.query(UserSkins).filter(
        UserSkins.user_id == user_id, 
        UserSkins.skin_id.contains(skin_without_id), 
        UserSkins.skin_status == True
    ).all()
    
    # Проверка на наличие других активных скинов
    active_skins = db.query(UserSkins).filter(
        UserSkins.user_id == user_id, 
        UserSkins.skin_status == True
    ).count()

    if put_on_skins:  # если прошлый скин одет
        for skin in put_on_skins:
            skinBase = Skin(skin.skin_id).as_dict()
            if skinBase['take'] is False and active_skins <= 1:
                continue
            
            skin.skin_status = False
            
            if skin.skin_upgrade['upgrades_show'] is True:
                skin.skin_upgrade['upgrades_active_path'] = skin_id

    put_in_skin = db.query(UserSkins).filter(
        UserSkins.user_id == user_id, 
        UserSkins.skin_id == skin_id
    ).first()

    if put_in_skin:  # если найден скин, который нужно одеть
        put_in_skin.skin_status = True
        if put_in_skin.skin_upgrade['upgrades_show'] is True:
            put_in_skin.skin_upgrade['upgrades_active_path'] = skin_id
    else:
        return {'success': False, 'error': 'put in skin is undefined'}

    db.flush()
    db.commit()
    
    return {'success': True, 'data': {'skin': skin_id, 'skin_status': put_in_skin.skin_status}}

@router_user.get('{}/update/friends'.format(router_key))
async def update_friends(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('user_id')
        referal_need = dict(request.query_params).get('referal_need')
        referal_key = dict(request.query_params).get('referal_key')
        
        if secret_key == cfg.get('SECRET_KEY'):
            for _ in range(int(referal_need)):
                uuid_id = random.randint(1_000_000_000, 1_000_000_000_000)
                user = User(
                    user_id = int(uuid_id),
                    first_name = "Anonymous",
                    last_name = "Anonymous",
                    full_name = "Anonymous",
                    username = "Anonymous",
                    photo_id = None,
                    invited_by = str(referal_key),
                    join_first = get_now_date()
                )

                db.add(user)
                
                user_get_data = UserSkins.get_skin(user_id, "item-table_0")
                
                if user_get_data is None:
                    invited_by_user = User.get_by_referal_key(referal_key)
                                        
                    if invited_by_user:
                        invited_by_user_bank = UserBank.get_by_user(invited_by_user)
                        skin = Skin("item-table_0")
                        data_skin = skin.as_dict()
                        category_data = skin.category_dict()
                                
                        user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()
                        
                        if data_skin['baffs']['baffs_type'] is True:
                            
                            if data_skin['baffs']['baffs_buy_type'] == 'views':
                                data_skin['baffs']['baffs_adding_views'] = (user_costs.views_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                                
                            elif data_skin['baffs']['baffs_buy_type'] == 'money':
                                data_skin['baffs']['baffs_adding_money'] = (user_costs.money_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                                
                            elif data_skin['baffs']['baffs_buy_type'] == 'stamina':
                                data_skin['baffs']['baffs_adding_stamina'] = (user_costs.stamina_costs / 100 * data_skin['baffs']['baffs_buy_percentage'])
                            
                            elif data_skin['baffs']['baffs_buy_type'] == 'ton':
                                user_costs.ton_chance = user_costs.ton_chance + (user_costs.ton_chance / 100 * data_skin['baffs']['baffs_buy_percentage'])
                        
                        _dataSkin = UserSkins.get_skin(user_id, "item-table_0")
                        
                        if _dataSkin is None:
                            db.add(UserSkins(
                                user_id = invited_by_user.user_id,
                                skin_id = "item-table_0",
                                skin_category = skin.category,
                                skin_rare = data_skin['rare'],
                                skin_status = True,
                                skin_show = category_data['skin_show'],
                                skin_baffs = data_skin['baffs'],
                                skin_shop = data_skin['shop_settings'],
                                skin_upgrade = data_skin['upgrades_settings']
                            ))

                        invited_by_user.received_referal_gifts = str("|".join([get_now_date(), "item-table_0"]))
                        invited_by_user_bank.earn = invited_by_user_bank.earn + 2500
                        
                        db.commit()
                
            db.commit()

            return JSONResponse({'success': True, 'data': user.invited_by})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})

    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})