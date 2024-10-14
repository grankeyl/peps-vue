from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from database.connection import db, Daily, User, UserSkins, UserCosts
from utils import get_now_date, get_now_date_without_time, Skin
from routes.user import changeSkinFunc

import json
from config import cfg

# Экземпляр APIRouter
router = APIRouter()
router_key = "/api/daily"

async def dailyCreates():
    '''
        Create Task in Database
    '''
    try:
        daily_json = {}
        
        try:
            with open('./../dailyArray.json', 'r', encoding='utf-8') as json_file:
                daily_json = json.load(json_file)
                
        except Exception as e:
            print(e)
        
        if daily_json:
            Daily.clear()
            for key, value in daily_json.items():
                db.add(Daily(
                    gift_uuid = int(key),
                    gift_type = value['gift_type'],
                    gift_amount = value['gift_amount'],
                    gift_skin = value['gift_skin']
                ))

        db.flush()
        db.commit()

        return { 'success': True }
    
    except Exception as e:
        print(e)
        return { 'success': False }

@router.get('{}/get_all'.format(router_key))
async def get_daily_all(request: Request):
    '''
        Get Daily in Database
    '''
    try:
        secret_key = dict(request.query_params).get('key')
        
        if secret_key == cfg.get('SECRET_KEY'):
            daily_gifts = Daily.get_daily_all()
            return {'success': True, 'daily': daily_gifts}
        else:
            return {'success': False, 'error': 'wrong key'}
    except Exception as e:
        print(e)
        return {'success': False}


@router.get('{}/get_gifts_stars'.format(router_key))
async def get_gifts_stars(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get("user_id")
        
        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()

            received_gifts = len(user.daily_gifts.split('|'))

            if user:
                gifts = Daily.get_daily_all()
                current_gift_index = 0
                for gift in gifts:
                    current_gift_index += 1
                    if current_gift_index > received_gifts:
                        if str(gift.get('gift_type')).lower() == "money":
                            user.earn_balance = user.earn_balance + int(gift.get('gift_amount'))
                        elif str(gift.get('gift_type')).lower() == "views":
                            user.views_balance = user.views_balance + int(gift.get('gift_amount'))
                        elif str(gift.get('gift_type')).lower() == "skin":
                            skin_id = gift.get('gift_skin')
                            
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
                            
                            _dataSkin = UserSkins.get_skin(user_id, skin_id)
                                                
                            if _dataSkin is None:
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
                                
                                await changeSkinFunc(user_id, skin_id)
            else:
                return JSONResponse({'success': False})
            
            db.flush()
            db.commit()
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})

        return JSONResponse({'success': True})
    except Exception as E:
        print(E)
        return JSONResponse({'success': False})


@router.get('{}/get_gift'.format(router_key))
async def get_daily_gift(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        user_id = params.get('user_id')
        
        if secret_key == cfg.get('SECRET_KEY'):

            user = db.query(User).filter(User.user_id == user_id).first()
            
            if user:
                if user.daily_last_date == get_now_date_without_time(): # дата проверка
                    return JSONResponse({'success': True, 'gift': None, 'gifts': user.daily_gifts.split('|')})
                
                daily_gifts = Daily.get_daily_all()

                if user.daily_gifts:
                    user_daily_gifts = list(user.daily_gifts.split('|'))
                else:
                    user_daily_gifts = []

                if len(list(user.daily_gifts.split('|'))) == len(daily_gifts):
                    return JSONResponse({'success': True, 'gift': None, 'gifts': user.daily_gifts.split('|')})

                current_gift = daily_gifts[len(user_daily_gifts)]

                user_daily_gifts.append(str(current_gift['gift_uuid']))

                user.daily_gifts = "|".join(list(user_daily_gifts))
                user.daily_last_date = get_now_date_without_time()

                if str(current_gift.get('gift_type')) == "skin":
                    skin_id = current_gift.get('gift_skin')
                    
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
                    
                    _dataSkin = UserSkins.get_skin(user_id, skin_id)
                                        
                    if _dataSkin is None:
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
                                
                        await changeSkinFunc(user_id, skin_id)
                
                db.flush()
                db.commit()
                return JSONResponse({'success': True, 'gift': current_gift, 'gifts': user.daily_gifts.split('|')})
            else:
                return JSONResponse({'success': False})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})

    except Exception as E:
        print(E)
        return {'success': False}