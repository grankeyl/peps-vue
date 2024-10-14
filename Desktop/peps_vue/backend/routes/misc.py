from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from bot.handlers.api import send_log, check_subscribe_to_channel, get_user_avatar, Stars
from database.connection import Invoices, db
from config import cfg

import base64
import json

# Экземпляр APIRouter
router = APIRouter()
router_key = "/api/misc"

@router.get('{}/sendLogAdmin'.format(router_key))
async def send_log_admin(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        type = params.get('type')
        params = json.loads(params.get('params'))
        
        if secret_key == cfg.get('SECRET_KEY'):
            await send_log(type, params)
            return JSONResponse({'success': True})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
        
    except:
        return JSONResponse({'success': False})

@router.get('{}/checkSubscribe'.format(router_key))
async def check_subscribe(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        user_id = params.get('user_id')
        channel_id = params.get('channel_id')
        
        if secret_key == cfg.get('SECRET_KEY'):
            isSubscribed = False
            isSubscribed = await check_subscribe_to_channel(user_id, channel_id)

            return JSONResponse({'success': True, 'isSubscribed': isSubscribed})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
    except:
        return JSONResponse({'success': False})

@router.get('{}/getAvatar'.format(router_key))
async def get_avatar(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        user_id = params.get('user_id')
        
        if secret_key == cfg.get('SECRET_KEY'):
            avatar = await get_user_avatar(user_id)
            if avatar:
                avatar_base64 = base64.b64encode(avatar.getvalue()).decode('utf-8')
                return JSONResponse({'success': True, 'avatar': ''.join(['data:image/png;base64,', avatar_base64])})
            else:
                return JSONResponse({'success': True, 'avatar': 'None'})
        else:
            return JSONResponse({'success': True, 'avatar': 'None'})
    except:
        return JSONResponse({'success': True, 'avatar': 'None'})

@router.get('{}/createStarsLink'.format(router_key))
async def create_stars_link(request: Request):
    
        '''
        
        invoice_params:
        
        {
            "invoiceType": "bandle",
            "isGift": true,
            
            "giftType": "money",
            "giftAmount": 250,
            
            "giftHasSkin": true,
            "giftSkin": "cap_3"
        }
        
        '''
        
    # try:
        params = dict(request.query_params)
        
        secret_key = params.get('key')
        userId = params.get('user_id')
        invoiceTitle = params.get('invoice_title')
        invoiceDescription = params.get('invoice_description')
        invoiceAmount = params.get('invoice_amount')
        invoicePhoto = params.get('invoice_photo')
        invoiceParams = params.get('invoice_params')
        
        if secret_key == cfg.get('SECRET_KEY'):
            stars = Stars(userId)
            stars_data = await stars.CreateInvoice(
                invoice_title=invoiceTitle,
                invoice_description=invoiceDescription,
                invoice_price=invoiceAmount,
                invoice_photo=invoicePhoto,
                invoice_params=invoiceParams
            )
            
            invoice_add = Invoices(
                user_id = userId,
                invoice_id = json.loads(invoiceParams)['invoice'].split('@')[0],
                invoice_params = invoiceParams,
                invoice_amount = invoiceAmount,
                invoice_status = "wait"
            )
            
            db.add(invoice_add)
            
            db.flush()
            db.commit()

            return JSONResponse({
                'success': True, 
                'data': {
                    'invoice_link': stars_data
                }
            })
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
    # except Exception as e:
    #     print(e)
    #     pass

@router.get('{}/getInvoice'.format(router_key))
async def getInvoice(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        invoice_id = params.get('invoice_id')

        if secret_key == cfg.get('SECRET_KEY'):
            invoice = db.query(Invoices).filter(Invoices.invoice_id == invoice_id).first()

            if invoice:
                return JSONResponse({'success': True, 'invoice': invoice.as_dict()})
            else:
                return JSONResponse({'success': False})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
    except Exception as E:
        print(E)
        pass

@router.get('{}/existsInvoice'.format(router_key))
async def is_exists_invoice(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        
        if secret_key == cfg.get('SECRET_KEY'):
            invoice_id = dict(request.query_params).get('invoice_id')
            return JSONResponse({'success': True, 'exists': Invoices.is_exist(invoice_id)})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
        
    except Exception as E:
        print(E)
        return JSONResponse({'success': False})

@router.get('{}/localization'.format(router_key))
async def localization(request: Request):
    try:
        secret_key = dict(request.query_params).get('key')
        
        if secret_key == cfg.get('SECRET_KEY'):
            with open('./../textsArray.json', 'r', encoding='utf-8') as local_file:
                localization_data = json.load(local_file)
            
            return JSONResponse({'success': True, 'localization': localization_data})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
        
    except Exception as E:
        print(E)
        return JSONResponse({'success': False})