from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from flask_login import current_user
from blog.models import User


users_app = Blueprint(name='users_app', import_name=__name__)
# USERS = {
#     1: 'Jake',
#     2: 'Shon',
#     3: 'Viktoria'
# }

@users_app.route('/', endpoint='list')
def users_list():

    users = User.query.all()
    return render_template('users/list.html', users=users,)

@users_app.route('/<int:user_id>/', endpoint='details')
def user_details(user_id: int):
    user = User.query.filter_by(id=user_id).one_or_none()
    if user is None:
        raise NotFound(f'User not found')
    return render_template('users/details.html', user=user)
    # try:
    #     select_user = USERS[user_id]
    # except KeyError:
    #     raise NotFound(f'User not found')
    # return render_template('users/details.html',
    #                        user_id=user_id, user_name=select_user)



