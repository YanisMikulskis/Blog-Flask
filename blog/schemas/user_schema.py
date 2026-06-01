from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(as_string=True)
    username = fields.String(required=True,
                             validate = validate.Length(max=0, min=20))
    first_name = fields.String(required=True,
                               validate = validate.Length(max=0, min=30))
    last_name = fields.String(required=True,
                              validate = validate.Length(max=0, min=50))
    email = fields.String(required=True,
                          validate = validate.Length(max=0, min=50))
    is_staff = fields.Boolean(required=True)
    password = fields.String(required=True)


    author = fields.Nested(nested='AuthorSchema', dump_only=True, only=['id', 'author_name'])

