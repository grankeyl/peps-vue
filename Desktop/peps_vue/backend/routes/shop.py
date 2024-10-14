from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from config import cfg

from database.connection import UserSkins, db

import json

router_shop = APIRouter()
router_key = "{}/shop".format(cfg.get("ROUTER_KEY"))

@router_shop.get('{}/shop/items'.format(cfg.get("ROUTER_KEY")))
async def items(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        user_id = dict(request.query_params).get('userId')
        
        if secret_key == cfg.get('SECRET_KEY'):
            with open('../skinsArray.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            with open('../names.json', 'r', encoding='utf-8') as json_file:
                names = json.load(json_file)

            stars = []
            money_views = []
            
            skins = db.query(UserSkins).filter(UserSkins.user_id == user_id).first()
            skins_list = skins.skin_list()

            for category in data.keys():
                versions = data[category].get('versions')

                if versions is not None:
                    for item_key in versions.keys():
                        if item_key not in skins_list:
                            item = versions[item_key]

                            if item['shop_settings'].get('shop_show'):
                                item['name'] = names[item['skin_id']]['name']
                                item['description'] = names[item['skin_id']]['description']
                                item['description_ru'] = names[item['skin_id']]['description_ru']
                                item['quantity_count'] = UserSkins.get_quantity_count(item['skin_id'])
                                price_type = item['shop_settings'].get('shop_price_type')
                                
                                try:
                                    item['shop_settings']['shop_price_cost'] = float(item['shop_settings']['shop_price_cost'])
                                except ValueError:
                                    item['shop_settings']['shop_price_cost'] = 0.0

                                if price_type == 'stars':
                                    stars.append(item)
                                elif price_type in ['money', 'views']:
                                    money_views.append(item)

            stars = sorted(stars, key=lambda x: x['shop_settings']['shop_price_cost'], reverse=True)
            money_views = sorted(money_views, key=lambda x: x['shop_settings']['shop_price_cost'], reverse=True)

            items = stars + money_views
            
            return JSONResponse({'success': True, 'items': items})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
    except:
        pass