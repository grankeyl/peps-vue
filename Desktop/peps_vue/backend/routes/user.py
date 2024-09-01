from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from config import cfg

from database.connection import db, User, UserSettings, UserCosts, UserSkins
from utils import get_now_date

import json
from utils import Skin

router_user = APIRouter()
router_key = "{}/user".format(cfg.get("ROUTER_KEY"))

@router_user.get('{}/create'.format(router_key))
async def user_create(request: Request):
    '''
    Create User in Database
    '''
    try:
        data = dict(request.query_params)

        user_id = data.get('user_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        full_name = data.get('full_name')
        username = data.get('username')
        photo_id = data.get('photo_id')
        
        existing_user = None

        try:
            existing_user = db.query(User).filter(User.user_id == int(user_id)).first()
        except Exception as E:
            print(E)
        
        if existing_user:
            return JSONResponse({ 'success': False, 'error': 'exists' })

        db.add(User(
            user_id = user_id,
            first_name = first_name,
            last_name = last_name,
            full_name = full_name,
            username = username,
            photo_id = photo_id
        ))

        db.add(UserSettings(
            user_id = user_id
        ))

        db.add(UserCosts(
            user_id = user_id
        ))

        with open('./constants.json') as json_file:
            constants = json.load(json_file)

        for skin_id in constants['default_skins']:
            skin = Skin(skin_id)
            data_skin = skin.as_dict()
            category_data = skin.category_dict()
            
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

        db.commit()

        return JSONResponse({ 'success': True, 'data': { 'user_id': user_id } })
    
    except Exception as e:
        print(e)
        return JSONResponse({ 'success': False, 'error': str(e) })


@router_user.get('{}/get'.format(router_key))
async def user_get(request: Request):
    '''
    Get User in Database
    '''
    try:
        user_id_str = dict(request.query_params).get('user_id')
        user_id = int(user_id_str)

        user_data = db.query(User).filter(User.user_id == user_id).first()
        user_settings_data = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
        user_costs_data = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()

        return JSONResponse({
            'success': True,
            'data': {
                'user': dict(user_data.as_dict()) if user_data else {},
                'settings': dict(user_settings_data.as_dict()) if user_settings_data else {},
                'costs': dict(user_costs_data.as_dict()) if user_costs_data else {}
            }
        })

    except Exception as e:
        return JSONResponse({ 'success': False, 'error': str(e) })


@router_user.get('{}/updateGame'.format(router_key))
async def update_game(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')
        views = dict(request.query_params).get('views')
        earn = dict(request.query_params).get('earn')
        ton = dict(request.query_params).get('ton')
        stamina = dict(request.query_params).get('stamina')

        print(views, earn, ton, stamina, user_id)

        user = db.query(User).filter(User.user_id == user_id).first()
        user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()

        if user and user_costs:
            user.views_balance = int(views)
            user.earn_balance = int(earn)
            user.ton_balance = float(ton)
        
            user_costs.stamina_now = int(stamina)

            db.commit()
            db.rollback()
        else:
            return JSONResponse({ 'success': False, 'error': "user not exsist" })

        return JSONResponse({'success': True})
        
    except Exception as e:
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/get/full_stamina'.format(router_key))
async def get_full_stamina(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')

        user = db.query(User).filter(User.user_id == user_id).first()
        user_costs = db.query(UserCosts).filter(UserCosts.user_id == user_id).first()

        if user:
            if user.full_stamina != 0:
                if not user.full_stamina:
                    user.full_stamina = 3

                user_costs.stamina_now = user_costs.stamina_costs
                user.full_stamina = int(user.full_stamina) - 1
                user.full_stamina_last_date = get_now_date()
                
                db.commit()

                return JSONResponse({ 'success': True, 'data': user_costs.stamina_costs })

            else:
                return JSONResponse({ 'success': False, 'error': 'not enough' })
        else:
            return JSONResponse({ 'success': False, 'error': 'user is not founded' })

    except Exception as e:
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/update/full_stamina'.format(router_key))
async def update_full_stamina(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')

        user = db.query(User).filter(User.user_id == user_id).first()

        if user:
            user.full_stamina = 3
            user.full_stamina_last_date = "None"
            
            db.commit()

            return JSONResponse({ 'success': True, 'data': user.full_stamina })
        else:
            return JSONResponse({ 'success': False, 'error': 'user is not founded' })
    except Exception as e:
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/update/buy'.format(router_key))
async def update_buy(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')
        type = dict(request.query_params).get('type')
        amount = dict(request.query_params).get('amount')

        user = db.query(User).filter(User.user_id == user_id).first()
        
        if type == "views":
            user.views_balance = int(user.views_balance) - int(amount)
            new_balance = user.views_balance
        elif type == "money":
            user.earn_balance = int(user.earn_balance) - int(amount)
            new_balance = user.earn_balance
        else:
            user.ton_balance = float(user.ton_balance) - float(amount)
            new_balance = user.ton_balance

        db.commit()
    
        return JSONResponse({'success': True, 'balance': new_balance})
    except Exception as e:
        return JSONResponse({ 'success': False, 'error': str(e) })

@router_user.get('{}/update/post_chances'.format(router_key))
async def update_post_chances(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')
        views_chance = dict(request.query_params).get('view_chance')
        money_chance = dict(request.query_params).get('money_chance')
        new_cost = dict(request.query_params).get('new_cost')
        
        type = None

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

        db.commit()

        return JSONResponse({'success': True, 'views_chance': int(views_chance), 'money_chance': int(money_chance)})

    except Exception as e:
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/update/settings'.format(router_key))
async def update_settings(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')
        language = dict(request.query_params).get('language')
        tap_animation = dict(request.query_params).get('tap_animation')
        new_tap_animation = False

        settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()

        if str(tap_animation).lower() == 'false': new_tap_animation = False
        else: new_tap_animation = True
        
        settings.tap_animation = new_tap_animation
        settings.language = str(language)

        db.commit()

        return JSONResponse({'success': True, 'settings': {'language': language, 'tap_animation': tap_animation}})
    
    except Exception as e:
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/getSkins'.format(router_key))
async def get_skins(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')

        skins = db.query(UserSkins).filter(UserSkins.user_id == user_id).all()

        skins_list = []

        with open('../categoriesArray.json') as json_file:
            categories = json.load(json_file)

        for skin in skins:
            skins_list.append(skin.as_dict())

        return JSONResponse({'success': True, 'skins': skins_list, 'categories': [x[0].upper() + x[1:] for x in categories]})
    
    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/getPutonSkins'.format(router_key))
async def get_puton_skins(request: Request):
    # try:
        user_id = dict(request.query_params).get('user_id')

        skins = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_status == True).all()

        return JSONResponse({'success': True, 'skins': [skin.as_dict() for skin in skins], 'skins_list': [skin.as_dict()['skin_id'] for skin in skins]})
    # except Exception as e:
    #     print(e)
    #     return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/upgradeSkin'.format(router_key))
async def upgrade_skin(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')
        skin_id = dict(request.query_params).get('skin_id')
        upgrade = dict(request.query_params).get('upgrade')

        if isinstance(upgrade, str):
            upgrade = json.loads(upgrade)

        skin = db.query(UserSkins).filter(UserSkins.user_id == user_id, UserSkins.skin_id == skin_id).first()
        skin.skin_upgrade = upgrade  # Now this should work fine

        db.commit()

        return JSONResponse({'success': True, 'upgrade': upgrade})

    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})

@router_user.get('{}/buySkin'.format(router_key))
async def buy_skin(request: Request):
    try:
        user_id = dict(request.query_params).get('user_id')
        skin_id = dict(request.query_params).get('skin_id')

        skin = Skin(skin_id)
        data_skin = skin.as_dict()
        category_data = skin.category_dict()
            
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

        db.commit()

        return JSONResponse({'success': True, 'skin': skin_id})

    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})
