

class Config:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOT_TOKEN = '5575858318:AAF3RdlwD61U9C5oXgec1TBYYx5Qa0bAdc4'
    
class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///debug.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///debug.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

Default_Config = ProductionConfig()
