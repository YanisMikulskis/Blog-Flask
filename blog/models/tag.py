import sqlalchemy.orm as so
from blog.extension import db

from sqlalchemy import String
from sqlalchemy.orm import relationship
from .article_tag import article_tag_association_table


class Tag(db.Model):
    __tablename__ = 'tags'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(String(32), nullable=False, default='', server_default='')
    articles = relationship('Article',
                            secondary=article_tag_association_table,
                            back_populates='tags')
