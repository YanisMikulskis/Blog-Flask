import sqlalchemy.exc
from flask.cli import with_appcontext
import click
from .extension import db
from .models import User













# @click.command('init-db')
# @with_appcontext
#
# def init_db_command():
#     '''
#     Terminal
#     '''
#
#     db.create_all()
#     print(f'База была пересоздана!')

@click.command('create-admin')
@with_appcontext

def create_admin():
    '''
    Run in your terminal:
    -> flask create-admin
    > created admin: <User #1 'admin'>
    '''
    from blog.models import User

    admin_user = User(username='admin-yanis', is_staff=True)
    admin_user.password = '1234567890' # в дальнейшем брать из переменной окружения

    db.session.add(admin_user)
    db.session.commit()
    print(f'created admin', admin_user)

@click.command('delete-admin')
@with_appcontext
def delete_admin():
    from blog.models import User

    admin_user = User.query.filter_by(username='admin-yanis').one_or_none()
    db.session.delete(admin_user)
    db.session.commit()
    print(f'admin has been deleted')
@click.command('create-users')
@with_appcontext

def create_users_command():
    '''
    terminal
    '''
    try:
        names_users = ['admin', 'james', 'vitek']
        for name_user in names_users:
            if name_user == 'admin':
                user = User(username='admin', is_staff = True)
            else:
                user = User(username = name_user, name = f'{name_user} human')

            db.session.add(user)
        db.session.commit()

        print(f'done! users created')
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        print(f'Команда уже была выполнена, юзеры существуют! Пересоздайте базу')

@click.command('drop-db')
@with_appcontext
def drop_db_command():
    db.drop_all()
    print(F'БД была удалена')


@click.command('check-db')
@with_appcontext

def check_db():
    from sqlalchemy import inspect
    ins = inspect(db.engine)
    table = ins.get_columns('users')
    from .models import User
    print(f'nаблы = {User.query.all()}')


