import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo-app.db'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass
