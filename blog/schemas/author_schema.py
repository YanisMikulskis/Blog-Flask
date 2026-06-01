from marshmallow import Schema, fields, validate, validates


class AuthorSchema(Schema):
    # Поля, которые будут в JSON
    id = fields.Integer(as_string=True)
    user_id = fields.Integer(required=True)
    # Вложенные схемы
    user = fields.Nested(nested='UserSchema',
                         dump_only=True,
                         only=['id', 'username'])
    articles = fields.Nested(nested='ArticleSchema',
                             dump_only=True,
                             only=['id', 'title'])
    #Доп поле
    author_name = fields.Method(serialize='get_author_name', dump_only=True)
    #
    def get_author_name(self, obj):
        return obj.user.username if obj.user else f'Author {obj.id}'

