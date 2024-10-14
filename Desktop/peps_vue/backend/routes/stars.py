from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from database.connection import Tasks, db, User
from config import cfg

import json

# Экземпляр APIRouter
router_stars = APIRouter()
router_stars_api = "/api/stars"

@router_stars.get('{}/shopBandles'.format(router_stars_api))
async def shop_bandles(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        user_id = params.get('user_id')
        type_bandle = params.get('type_bandle')
        amount_bandle = params.get('amount_bandle')
        
        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()
            
            if user:
                if type_bandle.lower() == 'views':
                    user.views_balance += int(amount_bandle)
                        
                elif type_bandle.lower() == 'money':
                    user.earn_balance += int(amount_bandle)
                
                if type_bandle.lower() == 'ton':
                    user.ton_balance += float(amount_bandle)
                    
                db.flush()
                db.commit()

                return JSONResponse({'success': True, 'balances': {'views': user.views_balance, 'earn': user.earn_balance, 'ton': user.ton_balance}})
            else:
                return JSONResponse({'success': False, 'error': 'user is not founded'})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
        
    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})
