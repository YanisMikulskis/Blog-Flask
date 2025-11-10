from flask import Blueprint,render_template
from werkzeug.exceptions import NotFound

articles_app = Blueprint('articles_app', __name__)


ARTICLES_ID = {
    1:'Flask',
    2:'Django',
    3:'Angular',
    4:'FastApi'
}

ARTICLES_TEXT = {ARTICLES_ID[1]: 'This is easy backend framework',
            ARTICLES_ID[2]: 'This is hard backend framework',
            ARTICLES_ID[3]: 'This is very hard typescript framework',
            ARTICLES_ID[4]: 'This is FastApi framework'}




@articles_app.route('/', endpoint='list')
def articles_list():
    return render_template('articles/list_articles.html', articles = ARTICLES_ID)


@articles_app.route('/<int:article_id>/', endpoint='details')
def articles_details(article_id: int):
    try:
        select_article = ARTICLES_TEXT[ARTICLES_ID[article_id]]
    except KeyError:
        return NotFound(f'Article not found')
    else:
        return render_template('articles/details_articles.html',
                        article_id=article_id,
                        select_article=select_article)

