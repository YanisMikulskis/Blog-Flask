import logging

from flask import Flask, request, g, render_template, redirect, url_for
from time import time
from werkzeug.exceptions import BadRequest
from .views.users import users_app
from .views.articles import articles_app
from .views.auth import auth_app

# from .models.database import *

from .commands import init_db_command, create_users_command,drop_db_command, check_db

from .extension import login_manager, db, migrate
from flask_migrate import Migrate
import os




def create_app() -> Flask:
    app = Flask(__name__) # экземпляр приложения
    is_docker = os.environ.get('IS_DOCKER')
    if is_docker == '0':
        cfg_name = 'DevConfig'
    else:
        cfg_name = os.environ.get('CONFIG_NAME')
    print(f'cf = {cfg_name}')
    app.config.from_object(f'blog.configs.{cfg_name}')


    print(f'cf = {cfg_name}')
    print(f'SQLALCHEMY_DATABASE_URI = {os.environ.get('SQLALCHEMY_DATABASE_URI')}')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SECRET_KEY"]='abcd'




    _add_extensions(app)
    _add_base_route(app)
    _add_context_processor(app)
    _add_blueprints(app)
    _add_commands(app)
    return app


def _add_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).one_or_none()

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth_app.login'))



def _add_base_route(app):
    @app.route('/', endpoint='home')
    def home_page():
        return render_template('home_page.html')

    @app.route('/my_page', endpoint='my_page')
    def my_page():
        return render_template('my_page.html',)



def _add_context_processor(app):
    @app.context_processor
    def inject_nav_data() -> dict:
        '''
        Для подсветки пунктов меню, если мы на текущей странице
        '''
        nav_items = [
            {'endpoint': 'home', 'label': 'Home'},
            {'endpoint': 'my_page', 'label': 'My page'},
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
                                     'articles_app.details']
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
            }

        ]
        return {'nav_items': nav_items}



def _add_blueprints(app) -> None:
    app.register_blueprint(users_app, url_prefix='/users')  # все url блупринта будут начинаться на то,
    # что мы кидаем в url_prefix
    app.register_blueprint(articles_app, url_prefix='/articles')
    app.register_blueprint(auth_app, url_prefix='/authentication')


def _add_commands(app) -> None:
# вызов команд из commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_users_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(check_db)
app = create_app()
