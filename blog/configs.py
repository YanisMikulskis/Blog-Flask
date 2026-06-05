import os
from check_docker import is_docker
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'abcd'
    WTF_CSRF_ENABLED = True
    FLASK_ADMIN_SWATCH = 'cosmo'

class DevConfig(BaseConfig):
    DEBUG = True
    if not is_docker:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    API_TITLE = 'Blog API'
    API_VERSION = 'V1'
    OPENAPI_VERSION = '3.0.3'
    # 3. НАСТРОЙКА OPENAPI (пути к документации)
    OPENAPI_URL_PREFIX = '/'  # Базовый путь для документации
    OPENAPI_SWAGGER_UI_PATH = '/swagger'  # Путь к Swagger UI
    OPENAPI_SWAGGER_URL = '/openapi.json'  # URL с JSON схемой
    OPENAPI_REDOC_PATH = '/redoc'  # Путь к ReDOC

    print(f'sql from configs = {SQLALCHEMY_DATABASE_URI}')


class TestingConfig(BaseConfig):
    TESTING = True



