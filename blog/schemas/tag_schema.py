from marshmallow import Schema, fields


class TagSchema(Schema):
    # class Meta:
    #     type_ = 'tag'
    #     self_view = 'tag_detail'
    #     self_view_kwargs = {'id': '<id>'}
    #     self_view_many = 'tag_list'
    id = fields.Integer(as_string=True)
    name = fields.String(allow_none=False, required=True)
    articles = fields.Nested(nested='ArticleSchema',
                            dump_only=True,
                            only=['id', 'title'])
    class Meta:
        field = ('id', 'fields')
        ordered = True