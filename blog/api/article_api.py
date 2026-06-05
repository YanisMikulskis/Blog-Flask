from blog.extension import db
from blog.models import Article
from blog.schemas.article_schema import ArticleSchema
from flask_smorest import Blueprint
from flask.views import MethodView




article_api_blp = Blueprint('article_api', 'article_api')

@article_api_blp.route('/')
class ArticleList(MethodView):

    @article_api_blp.response(200, ArticleSchema(many=True))
    def get(self):
        return Article.query.all()

    @article_api_blp.arguments(ArticleSchema)
    @article_api_blp.response(201, ArticleSchema)
    def post(self, data):
        article = Article(**data)
        db.session.add(article)
        db.session.commit()
        return Article

@article_api_blp.route('/<int:article_id>')
class ArticleDetail(MethodView):
    @article_api_blp.response(200, ArticleSchema)
    def get(self, article_id):
        return Article.query.get_or_404(article_id)
    @article_api_blp.arguments(ArticleSchema)
    @article_api_blp.response(200, ArticleSchema)
    def patch(self, data, article_id):
        article = Article.query.get_or_404(article_id)
        for key, val in data.items():
            setattr(article, key, val)
        db.session.commit()
        return article

    def delete(self, article_id):
        article = Article.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()
        return {'message':'deleted'}