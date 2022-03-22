from os import getenv,path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv('LOCAL_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {
    'echo': True,
    'pool_size': 10,
    'max_overflow': 10,
    'pool_recycle': 3600,
    'pool_timeout': 10,
    'pool_pre_ping': True
    }

class devConfig(Config):
    TESTING = True
    DEBUG = True

class testConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('TEST_DATABASE_URI')
    DEBUG = True    

class stageConfig(Config):
    TESTING = True
    DEBUG = True
    AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
    ACL = 'public-read'
    FLASKS3_BUCKET_NAME = getenv('FLASKS3_BUCKET_NAME')
    FLASKS3_REGION = getenv('FLASKS3_REGION') 

    
class prodConfig(Config):
    DEBUG = False
    TESTING = False