import logging

from flask import Flask, request, g, render_template
from time import time
from werkzeug.exceptions import BadRequest
from .views.users import users_app
from .views.articles import articles_app
from .models.database import *

from .commands import init_db_command, create_users_command,drop_db_command, check_db


import os





def create_app() -> Flask:
    app = Flask(__name__) # экземпляр приложения
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app) # инициализация бд

    from .models import User
    _add_base_route(app)
    _add_context_processor(app)
    _add_blueprints(app)
    _add_commands(app)
    return app




def _add_base_route(app):
    @app.route('/', endpoint='home')
    def home_page():
        return render_template('home_page.html')

    @app.route('/my_page', endpoint='my_page')
    def my_page():
        return render_template('index.html')



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
            }
        ]
        return {'nav_items': nav_items}



def _add_blueprints(app) -> None:
    app.register_blueprint(users_app, url_prefix='/users')  # все url блупринта будут начинаться на то,
    # что мы кидаем в url_prefix
    app.register_blueprint(articles_app, url_prefix='/articles')


def _add_commands(app) -> None:
# вызов команд из commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_users_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(check_db)
app = create_app()
