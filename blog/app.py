from flask import Flask, render_template, redirect, url_for

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



def create_app() -> Flask:
    app = Flask(__name__) # экземпляр приложения
    if not is_docker:
        cfg_name = 'DevConfig'
    else:
        cfg_name = os.environ.get('CONFIG_NAME')
    app.config.from_object(f'blog.configs.{cfg_name}')

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
    flask_bcrypt.init_app(app)
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
    app.register_blueprint(users_app, url_prefix='/users')  # все url блупринта будут начинаться на то,
    # что мы кидаем в url_prefix
    app.register_blueprint(articles_app, url_prefix='/articles')
    app.register_blueprint(auth_app, url_prefix='/authentication')
    app.register_blueprint(authors_app, url_prefix='/authors')
    app.register_blueprint(tags_app, url_prefix ='/tags')


def _add_commands(app) -> None:
# вызов команд из commands
#     app.cli.add_command(init_db_command)
    app.cli.add_command(create_users_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(check_db)
    app.cli.add_command(create_admin)
    app.cli.add_command(delete_admin)
    app.cli.add_command(create_tags)
app = create_app()
