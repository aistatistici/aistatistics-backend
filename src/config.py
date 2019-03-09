import os

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:

    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "aistatistics_key")
    MONGO_URI = "mongodb://localhost:27017/aistatistici"
    SQLALCHEMY_DATABASE_URI = "postgres://aiadmin:ai0205@127.0.0.1:5432/aistatistici"


class Production(Config):

    pass


class Development(Config):

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(Config):

    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_dict = {
    'development': Development,
    'production': Production,
    'testing': Testing,
}

MEDIA_ROOT = '/tmp/aistatistici/static/mediafiles'
STATIC_ROOT = '/tmp/aistatistici/static/staticfiles'

key = Config.SECRET_KEY


