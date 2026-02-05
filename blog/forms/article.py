from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     validators,
                     SubmitField,
                     SelectMultipleField)
from flask_login import current_user
class CreateArticleForm(FlaskForm):

    title_form = StringField(
        'Title',
        [validators.DataRequired()]
    )
    body_form = TextAreaField(
        'Body',
        [validators.DataRequired()]
    )
    submit_form = SubmitField('Publish')

    tags_form = SelectMultipleField('Tags', coerce=int)
