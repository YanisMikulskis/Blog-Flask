from marshmallow import Schema, fields, validate
from .author_schema import AuthorSchema
from .tag_schema import TagSchema

class ArticleSchema(Schema):
    id = fields.Integer(as_string=True)
    author_id = fields.Integer(required=True)
    title = fields.String(required=True,
                          validate=validate.Length(min=1, max=200),
                          )
    body = fields.String(required=True,
                         validate=validate.Length(min=1))
    # Временные метки (только для чтения)
    dt_created = fields.DateTime(dump_only=True, format='iso', )
    dt_updated = fields.DateTime(dump_only=True, format='iso')
    # Вложенные схемы
    author = fields.Nested(nested='AuthorSchema',
                           dump_only=True,
                           only=['id', 'user_id', 'author_name'])
    tags = fields.Nested(nested='TagSchema',
                         many=True,
                         dump_only=True,
                         only=['id', 'name'])