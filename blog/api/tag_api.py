from blog.extension import db
from blog.models import Tag
from blog.schemas.tag_schema import TagSchema
from flask_smorest import Blueprint
from flask.views import MethodView


tags_api_blp = Blueprint('tag_api', 'tag_api')
# экземпляр класса Блупринта создаем на месте (сразу перед использвоание в роутах)
@tags_api_blp.route('/')
class TagList(MethodView):
    # GET запрос — получить все теги
    @tags_api_blp.response(200, TagSchema(many=True))
    def get(self):
        return Tag.query.all()

    @tags_api_blp.arguments(TagSchema) # принимаем JSON по схеме ТэгСхема
    @tags_api_blp.response(201, TagSchema) # возвращаем созданный тэг с кодом
    def post(self, data):
        tag = Tag(**data)
        db.session.add(tag)
        db.session.commit()
        return Tag

@tags_api_blp.route('/<int:tag_id>')
class TagDetail(MethodView):
    @tags_api_blp.response(200, TagSchema) #many=True отсутствует, так как мы хотим получить только один тэг
    def get(self, tag_id):
        return Tag.query.get_or_404(tag_id)

    @tags_api_blp.arguments(TagSchema)
    @tags_api_blp.response(200, TagSchema)
    def patch(self, data, tag_id):
        tag = Tag.query.get_or_404(tag_id)
        for key, value in data.items():
            setattr(tag, key, value)
        db.session.commit()
        return tag

    def delete(self, tag_id):
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return {'message': 'deleted'}
