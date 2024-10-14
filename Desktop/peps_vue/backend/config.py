from suprconfig.config import Config

cfg = Config("config.json")

def CreateConfig():
    cfg.add("ROUTER_KEY", "/api")
    
    # test public - 7223189423:AAH8obBt13Kt_EevzRQpOACL06NYEUjS9lA
    # test private - 5000799708:AAGSAhWwwy7qYRcHzfajAQfQv-qF6rcJnKA
    # test private (win) - 2200536971:AAE4OSB-svJv6cVx3DVLOo47zYfiYuY7PG8
    
    cfg.add("LOCAL_STATUS", True)
    cfg.add("DEVELOPER_STATUS", True)
    
    if cfg.get("LOCAL_STATUS") == True:
        cfg.add("BOT_TOKEN", "5000799708:AAGSAhWwwy7qYRcHzfajAQfQv-qF6rcJnKA")
        cfg.add("DOMAIN", "http://192.168.0.123:8080")
        cfg.add("DOMAIN_ORIG", "https://5ec6-95-59-121-213.ngrok-free.app")
    else:
        cfg.add("BOT_TOKEN", "2200536971:AAE4OSB-svJv6cVx3DVLOo47zYfiYuY7PG8")
        cfg.add("DOMAIN", "http://185.125.102.222:8080")
        cfg.add("DOMAIN_ORIG", "https://5ec6-95-59-121-213.ngrok-free.app")
    
    if cfg.get("DEVELOPER_STATUS") == True:
        cfg.add("ADMINS_IDS", [5000401812])
        cfg.add("LOGS_CHANNEL_ID", -1005000196871)
        cfg.add("CHANNEL_RU_ID", -1005000770519)
        cfg.add("CHANNEL_EN_ID", -1005000574111)
    else:
        cfg.add("ADMINS_IDS", [1460617279, 2106187940, 5000401812])
        cfg.add("LOGS_CHANNEL_ID", -1002180849899)
        cfg.add("CHANNEL_RU_ID", -1002146032263)
        cfg.add("CHANNEL_EN_ID", -1002128815254)
        
        
    cfg.add("SECRET_KEY", "FQ2(5&2*H^QwV")