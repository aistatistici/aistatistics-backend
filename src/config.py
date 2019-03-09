import os

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:

    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "aistatistics_key")
    MONGO_URI = "mongodb://localhost:27017/aistatistici"


class Production(Config):

    pass


class Development(Config):

    DEBUG = True


class Testing(Config):

    DEBUG = True
    TESTING = True


config_dict = {
    'development': Development,
    'production': Production,
    'testing': Testing,
}

MEDIA_ROOT = '/opt/aistatistici/static/staticfiles'
STATIC_ROOT = '/opt/aistatistici/static/mediafiles'

key = Config.SECRET_KEY


