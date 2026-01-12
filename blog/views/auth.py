from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from blog.extension import db
from blog.models import User
from blog.forms.user import RegistrationForm, LoginForm


auth_app = Blueprint(name='auth_app', import_name=__name__)

login_page = 'auth_app.login'



# @auth_app.route('/', endpoint='login', methods=['GET', 'POST'])
# def login():
#     # return 'WIP'
#     if current_user.is_authenticated:
#         return redirect('home')
#     form = LoginForm(request.form)
#
#     if request.method == 'POST' and form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).one_or_none()
#         if user is None:
#             return render_template(f'auth/register.html', form=form, error='user not exists')
#         elif not user.validate_password(form.password.data):
#             return render_template(f'auth/register.html', form=form, error='invalid password')
#         login_user(user)
#         redirect(url_for('home'))
#     return render_template(f'auth/register.html', form=form)




    # if request.method == 'GET': # првоерка, так как в начале мы просто открывапем страницу
    #     return render_template('auth/login.html')
    #
    # username = request.form.get('username')
    # password = request.form.get('password')
    #
    # if not username:
    #     return render_template('auth/login.html', error='username not passed')
    #
    # user = User.query.filter_by(username=username).one_or_none()
    # if user is None:
    #     return render_template('auth/login.html', error=f'no user {username}!')
    #
    # login_user(user)
    #
    # return redirect(url_for('my_page'))
@auth_app.route('/login-as/', methods=['POST', 'GET'], endpoint='login-as')
def login_as():
    if not (current_user.is_autheticated and current_user.is_staff):
        raise NotFound
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = User.query.filter_by(username=form.username.data).one_or_none()
        if username is None:
            return render_template('auth/login.html', form=form,
                                   error='Dear admin! User is not exists')
        login_user(username)
        return redirect(url_for('home'))
    return render_template('auth/login.html', form=form)

@auth_app.route('/', methods=['POST', 'GET'], endpoint='login')
def login():


    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).one_or_none()

        if user is None:
            return render_template('auth/login.html', form=form,
                                   error='Dear admin! User is not exists')
        elif not user.validate_password(form.password.data):
            return render_template('auth/login.html', form=form,
                                   error='Dear admin! invalid password')
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('auth/login.html', form=form)

@auth_app.route('/logout/', endpoint='logout')
@login_required # доступ только для авторизованных
def logout():
    logout_user()
    return redirect(url_for('home'))



@auth_app.route('/secret/', endpoint='secret')
@login_required
def secret_view():
    return 'secret data'





@auth_app.route('/register/', endpoint='register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('home')

    error = None
    form = RegistrationForm(request.form) #request.form это данные, которые мы отправляем на сервер
    if request.method == 'POST' and form.validate_on_submit():
        '''
        form.validate_on_submit()
        Это метод Flask-WTF (WTForms + интеграция с Flask).
        Он делает две вещи одновременно:
        Проверяет, что метод запроса — POST.
        Вызывает form.validate() — проверку всех валидаторов, которые вы прописали в форме (DataRequired, Email, Length и т.д.).
        Возвращает True, если:
        Запрос POST и все поля прошли валидацию.
        Возвращает False, если:
        Метод GET
        Или данные формы невалидны (например, пустой email, короткий пароль и т.д.)
        '''
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append(f'User already exists!') #добавить свой текст во встреонную функцию ошибки
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append(f'email already exists!')
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            is_staff = False
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception('Could not create user!')
            error = f'could not create user!'
        else:
            current_app.logger.info(f'created user {user}')
            login_user(user)
            return redirect(url_for(f'home'))
    return render_template('auth/register.html', form=form,error=error)




