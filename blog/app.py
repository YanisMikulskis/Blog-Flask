from flask import Flask, render_template, redirect, url_for
from blog.admin import admin
from .views.users import users_app
from .views.articles import articles_app
from .views.auth import auth_app
from .views.authors import authors_app
from .views.tags import tags_app
from .commands import (create_users_command,
                       drop_db_command,
                       check_db,
                       create_admin,
                       delete_admin,
                       create_tags)
from .extension import login_manager, db, migrate
from .security import flask_bcrypt


import os

from check_docker import is_docker

#блупринты для api
from flask_smorest import Api
from .api.tag_api import tags_api_blp
from .api.article_api import article_api_blp
from .api.author_api import author_api_blp
from .api.user_api import user_api_blp


from flask_openapi3 import OpenAPI, Tag, Info


def create_app() -> Flask:

    app = Flask(__name__)
    # 1. ЗАГРУЗКА КОНФИГУРАЦИИ
    if not is_docker:
        cfg_name = 'DevConfig'
    else:
        cfg_name = os.environ.get('CONFIG_NAME')
    app.config.from_object(f'blog.configs.{cfg_name}')

    print(f'ВЫБрАН КОНФИГ {cfg_name}')



    # 5. Инициализация расширений
    _add_extensions(app)
    # 6. Добавление обычных маршрутов
    _add_base_route(app)
    _add_context_processor(app)
    _add_blueprints(app)
    _add_commands(app)
    # 7. Добавление API эндпоинтов
    _add_api_routes(app)
    return app






def _add_extensions(app):
    # расширения для БД и миграций
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    # аутентификация
    login_manager.init_app(app)
    flask_bcrypt.init_app(app)
    # админка
    admin.init_app(app)
    # Загрузчик пользователя для Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).one_or_none()

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth_app.login'))



def _add_base_route(app):
    """
    Добавляет базовые маршруты для HTML страниц
    """
    @app.route('/', endpoint='home')
    def home_page():
        return render_template('home_page.html')

    @app.route('/my_page', endpoint='my_page')
    def my_page():
        return render_template('my_page.html',)



def _add_context_processor(app):
    """
    Добавляет контекстный процессор для навигации
    """
    @app.context_processor
    def inject_nav_data() -> dict:
        '''
        Для подсветки пунктов меню, если мы на текущей странице
        '''
        nav_items = [
            {'endpoint': 'home',
             'label': 'Home'},
            {'endpoint': 'my_page',
             'label': 'My page'},
            {
                'endpoint': 'users_app.list',
                'label': 'Users',
                'active_endpoints': ['users_app.list',
                                     'users_app.details'],
            },
            {
                'endpoint': 'articles_app.list',
                'label': 'Articles',
                'active_endpoints': ['articles_app.list',
                                     'articles_app.details',
                                     'articles_app.create']
            },
            {
                'endpoint': 'auth_app.login',
                'label': 'Login',
                'active_endpoint': 'auth_app.login',

            },

            {
                'endpoint': 'auth_app.logout',
                'label': 'Logout',
                'active_endpoint': 'auth_app.logout'
            },

            {
                'endpoint': 'auth_app.register',
                'label': 'Register',
                'active_endpoint': 'auth_app.register'
            },
            {
                'endpoint': 'authors_app.list',
                'label':'Authors',
                'active_endpoint': 'authors_app.list'
            },
            {
                'endpoint': 'tags_app.list',
                'label': 'Tags',
                'active_endpoint': 'tags_app.list'
            }

        ]
        return {'nav_items': nav_items}



def _add_blueprints(app) -> None:
    """
    Регистрирует все обычные Blueprint'ы (для HTML страниц)
    """
    app.register_blueprint(users_app, url_prefix='/users')  # все url блупринта будут начинаться на то,
    # что мы кидаем в url_prefix
    app.register_blueprint(articles_app, url_prefix='/articles')
    app.register_blueprint(auth_app, url_prefix='/authentication')
    app.register_blueprint(authors_app, url_prefix='/authors')
    app.register_blueprint(tags_app, url_prefix ='/tags')



def _add_commands(app) -> None:
    """
    Добавляет CLI команды
    """
    app.cli.add_command(create_users_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(check_db)
    app.cli.add_command(create_admin)
    app.cli.add_command(delete_admin)
    app.cli.add_command(create_tags)

def _add_api_routes(app):
    """
    Регистрирует API эндпоинты с документацией
    """
    # app.register_api(tags_api_blp)
    # app.register_api(article_api_blp)
    # app.register_api(author_api_blp)
    # app.register_api(user_api_blp)


    # app.config['API_TITLE'] = 'Blog API'
    # app.config['API_VERSION'] = 'V1'
    # app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['API_TITLE'] = 'Blog API'
    app.config['API_VERSION'] = 'V1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    # 3. НАСТРОЙКА OPENAPI (пути к документации)
    app.config['OPENAPI_URL_PREFIX'] = '/'  # Базовый путь для документации
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'# Отсюда берем
                                                                                        # интерфейс для Swagger
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger' # Путь к Swagger таблицам
    app.config['OPENAPI_SWAGGER_URL'] = '/openapi.json'  # URL с JSON схемой
    app.config['OPENAPI_REDOC_PATH'] = '/redoc'  # Путь к ReDOC
    api = Api(app)
    #
    api.register_blueprint(tags_api_blp, url_prefix = '/tag_api')
    api.register_blueprint(article_api_blp, url_prefix='/article_api')
    api.register_blueprint(author_api_blp, url_prefix='/author_api')
    api.register_blueprint(user_api_blp, url_prefix='/user_api')


    print('++++++++++++++++++++')
    print(f"\n=== КОНФИГУРАЦИЯ API ===")
    print(f"API_TITLE: {app.config.get('API_TITLE')}")
    print(f"API_VERSION: {app.config.get('API_VERSION')}")
    print(f"OPENAPI_VERSION: {app.config.get('OPENAPI_VERSION')}")
    print(f"OPENAPI_URL_PREFIX: {app.config.get('OPENAPI_URL_PREFIX')}")
    print(f"OPENAPI_SWAGGER_UI_PATH: {app.config.get('OPENAPI_SWAGGER_UI_PATH')}")
    print(f"========================\n")
    print('\n=== ЗАРЕГИСТРИРОВАННЫЕ МАРШРУТЫ ===')
    for rule in app.url_map.iter_rules():
        if 'swagger' in rule.rule or 'openapi' in rule.rule or 'redoc' in rule.rule:
            print(f'✅ ДОКУМЕНТАЦИЯ: {rule.endpoint}: {rule.rule}')
app = create_app()
