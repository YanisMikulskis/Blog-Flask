import sqlalchemy.orm as so

from blog.extension import db
from sqlalchemy import String, Integer, Table, ForeignKey, Column


article_tag_association_table = Table(
    'article_tag_association',
    db.metadata,
    Column('article_id',
           Integer,
           ForeignKey('articles.id'),
           nullable=False),
    Column('tag_id',
           Integer,
           ForeignKey('tags.id'),
           nullable=False)

)


