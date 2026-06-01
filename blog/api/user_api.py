from blog.api.tag_api import tags_api_blp
from blog.extension import db
from blog.models import User
from blog.schemas.user_schema import UserSchema
from flask_smorest import Blueprint
from flask.views import MethodView

user_api_blp = Blueprint('user_api', 'user_api')
@user_api_blp.route('/')
class UserList(MethodView):
    @user_api_blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.all()

    @user_api_blp.arguments(UserSchema)
    @user_api_blp.response(201, UserSchema)
    def post(self, data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return User