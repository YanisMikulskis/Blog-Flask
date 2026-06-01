from blog.api.tag_api import tags_api_blp
from blog.extension import db
from blog.models import Author
from blog.schemas.author_schema import AuthorSchema
from flask_smorest import Blueprint
from flask.views import MethodView



author_api_blp = Blueprint('author_api', 'author_api')
@author_api_blp.route('/')
class AuthorList(MethodView):
    @author_api_blp.response(200, AuthorSchema(many=True))
    def get(self):
        return Author.query.all()

    @author_api_blp.arguments(AuthorSchema)
    @author_api_blp.response(201, AuthorSchema)
    def post(self, data):
        author = Author(**data)
        db.session.add(author)
        db.session.commit()
        return Author

@author_api_blp.route('<int:author_id>')
class AuthorDetail(MethodView):
    @author_api_blp.response(200, AuthorSchema)
    def get(self, author_id):
        author = Author.query.get_or_404(author_id)
        return author

    @author_api_blp.arguments(AuthorSchema)
    @author_api_blp.response(201, AuthorSchema)
    def patch(self, data, author_id):
        author = Author.query.get_or_404(author_id)
        for key, val in data.items():
            setattr(author, key, val)
        db.session.commit()
        return author

    def delete(self, author_id):
        db.session.delete(Author.query.get_or_404(author_id))
        db.session.commit()
        return {'message': 'deleted'}

