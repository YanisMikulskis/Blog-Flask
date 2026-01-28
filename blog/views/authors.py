from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from blog.models import Author

authors_app = Blueprint(name='authors_app', import_name=__name__)

@authors_app.route('/', endpoint='list')
def authors_list():
    authors = Author.query.all()
    return render_template('authors/list.html', authors=authors)