from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage

from app import bot, dp
from database.connection import User, UserSkins, Invoices, db, UserCosts
from routes.user import changeSkinFunc
from utils import Skin

import json

__all__ = ['dp']

''' TELEGRAM STARS CHECK PAYMENT '''
        
@dp.pre_checkout_query()
async def checkout_handler(checkout_query: PreCheckoutQuery):
    await checkout_query.answer(ok=True)
    
@dp.message(F.successful_payment)
async def star_payment(message):
    user_id = message.successful_payment.provider_payment_charge_id.split('_')[0]
    invoice_payload = message.successful_payment.invoice_payload
    
    user = db.query(User).filter(User.user_id == user_id).first()
    
    invoice_payload_id = None
    
    if user:
        if invoice_payload is not None:
            invoice_payload = json.loads(invoice_payload)
            invoice_payload_id = invoice_payload['invoice'].split('@')[0]
            invoice_payload_arg = invoice_payload['invoice'].split('@')[1]
            
            if invoice_payload['isGift'] is True:
                
                if invoice_payload_arg == 'speedupStamina':
                    user.full_stamina = 3
                    user.full_stamina_last_date = "None"
                    
                elif invoice_payload_arg == 'shopSkin':
                    if invoice_payload['giftHasSkin'] is not False:
                        skin = Skin(invoice_payload['giftSkin'])
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
                        
                        _dataSkin = UserSkins.get_skin(user_id, invoice_payload['giftSkin'])
                                            
                        if _dataSkin is None:
                            db.add(UserSkins(
                                user_id = user_id,
                                skin_id = invoice_payload['giftSkin'],
                                skin_category = skin.category,
                                skin_rare = data_skin['rare'],
                                skin_status = True,
                                skin_show = category_data['skin_show'],
                                skin_baffs = data_skin['baffs'],
                                skin_shop = data_skin['shop_settings'],
                                skin_upgrade = data_skin['upgrades_settings']
                            ))
                        
                            await changeSkinFunc(user_id, invoice_payload['giftSkin'])
                    
                elif invoice_payload_arg == 'upgradeSkin':
                    pass
                
                elif invoice_payload_arg == 'dailyAll':
                    pass
                
                elif invoice_payload_arg == 'buyFriends':
                    pass
                        
                else:
                    gift_type = invoice_payload['giftAmount'].split('|')[0]
                    gift_amount = invoice_payload['giftAmount'].split('|')[1]
                    
                    if gift_type in ["views", "money", "ton"]:
                        user.update_balance(gift_type, f"+{gift_amount}")
                    
                    if invoice_payload['giftHasSkin'] is not False:
                        skin = Skin(invoice_payload['giftSkin'])
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
                    
                        _dataSkin = UserSkins.get_skin(user_id, invoice_payload['giftSkin'])
                                            
                        if _dataSkin is None:
                            db.add(UserSkins(
                                user_id = user_id,
                                skin_id = invoice_payload['giftSkin'],
                                skin_category = skin.category,
                                skin_rare = data_skin['rare'],
                                skin_status = True,
                                skin_show = category_data['skin_show'],
                                skin_baffs = data_skin['baffs'],
                                skin_shop = data_skin['shop_settings'],
                                skin_upgrade = data_skin['upgrades_settings']
                            ))
                        
                            await changeSkinFunc(user_id, invoice_payload['giftSkin'])

    if invoice_payload_id:
        invoice = db.query(Invoices).filter(Invoices.invoice_id == invoice_payload_id).first()
        invoice.invoice_status = "paid"
        
    db.flush()
    db.commit()
    
    print("yes!", user_id)
    
''' TELEGRAM STARS CHECK PAYMENT '''