from suprconfig.config import Config

cfg = Config("config.json")

def CreateConfig():
    cfg.add("ROUTER_KEY", "/api")