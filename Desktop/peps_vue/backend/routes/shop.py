from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from config import cfg
import json

shop = APIRouter()
router_key = "{}/shop".format(cfg.get("ROUTER_KEY"))

@shop.get('{}/shop/items'.format(cfg.get("ROUTER_KEY")))
async def items(request: Request):
    with open('../skinsArray.json') as json_file:
        data = json.load(json_file)

    with open('../names.json') as json_file:
        names = json.load(json_file)

    stars = []
    money_views = []

    for category in data.keys():
        versions = data[category].get('versions')

        if versions is not None:
            for item_key in versions.keys():
                item = versions[item_key]

                if item['shop_settings'].get('shop_show'):
                    item['name'] = names[item['skin_id']]['name']
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