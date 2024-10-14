from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from database.connection import db, Daily, User, UserSkins
from utils import get_now_date, get_now_date_without_time, Skin

import json
from config import cfg

# Экземпляр APIRouter
router_chest = APIRouter()
router_key = "/api/chests"


@router_chest.get('{}/chests_get'.format(router_key))
async def chestsGet(request: Request):
    '''
        Get Chests
    '''
    try:
        secret_key = dict(request.query_params).get('key')
        
        if secret_key == cfg.get('SECRET_KEY'):
            chests_json = {}
            
            try:
                with open('./../chestsArray.json', 'r', encoding='utf-8') as json_file:
                    chests_json = json.load(json_file)
                    
            except Exception as e:
                print(e)

            return { 'success': True, 'data': chests_json }
        else:
            return { 'success': False, 'error': 'wrong key' }
    
    except Exception as e:
        print(e)
        return { 'success': False }