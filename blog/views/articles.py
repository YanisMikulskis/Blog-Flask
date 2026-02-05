from flask import Blueprint,render_template, request, current_app, redirect, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from blog.models import Article, Author,Tag
from blog.extension import db
from flask_login import login_required, current_user
from blog.forms.article import CreateArticleForm
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
    articles = Article.query.all()
    return render_template('articles/list_articles.html',
                           articles = articles)


@articles_app.route('/<int:article_id>/', endpoint='details')
def articles_details(article_id: int, delete_article=False):
    if delete_article:
        article = db.session.get(Article, article_id)
        if article is None:
            raise NotFound
        db.session.delete(article)
        db.session.commit()
    else:
        article = (Article.query.filter_by(id=article_id)
                   .options(joinedload(Article.tags))
                   .one_or_none())
        if article is None:
            raise NotFound
    return render_template('articles/details_articles.html',
                           article=article)


@articles_app.route('/create/', endpoint='create', methods=['GET', 'POST'])
@login_required
def create_articles():
    error = None
    form = CreateArticleForm(request.form)
    form.tags_form.choices = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    if request.method == 'POST' and form.validate_on_submit():


        author = current_user.author
        if author is None:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.commit()

        article = Article(title=form.title_form.data.strip(),
                          body=form.body_form.data,
                          author = author)

        if form.tags_form.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags_form.data))
            for tag in selected_tags:
                article.tags.append(tag)

        print(f'article = {article}')
        db.session.add(article)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            current_app.logger.exception('no create article')
            error = 'no create article'
        else:
            return redirect(url_for('articles_app.details', article_id=article.id))

    return render_template('articles/create_articles.html', error=error, form=form)
