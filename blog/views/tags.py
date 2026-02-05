from flask import Blueprint, render_template, request
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from blog.models import Tag, Article

from blog.extension import db
tags_app = Blueprint('tags_app', __name__)

@tags_app.route('/', endpoint = 'list')
def tags_list():
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

@tags_app.route('/<int:tag_id>/', endpoint='tags_articles')
def tags_articles(tag_id: int):
    tag = Tag.query.filter_by(id=tag_id).options(joinedload(Tag.articles)).one_or_none()
    if tag is None:
        raise NotFound
    return render_template('tags/tags_articles.html', tag=tag)

