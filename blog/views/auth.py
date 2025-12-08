from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.exceptions import NotFound
from blog.models import User

auth_app = Blueprint(name='auth_app', import_name=__name__)

login_page = 'auth_app.login'



@auth_app.route('/', endpoint='login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        return render_template('auth/login.html', error='username not passed')

    user = User.query.filter_by(username=username).one_or_none()
    if user is None:
        return render_template('auth/login.html', error=f'no user {username}!')

    login_user(user)

    return redirect(url_for('my_page'))



@auth_app.route('/logout/', endpoint='logout')
@login_required # доступ только для авторизованных
def logout():
    logout_user()
    return redirect(url_for('home'))



@auth_app.route('/secret/', endpoint='secret')
@login_required
def secret_view():
    return 'secret data'




__all__ = {
    'login_manager',
    'auth_app'
}