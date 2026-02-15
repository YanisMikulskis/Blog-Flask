import datetime
from xmlrpc.client import DateTime

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from blog.extension import db

from sqlalchemy import func
from datetime import datetime, timezone

from .article_tag import article_tag_association_table
class Article(db.Model):
    __tablename__ = 'articles'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    author_id: so.Mapped[int] = so.mapped_column(ForeignKey('authors.id'))
    author = relationship('Author', back_populates='articles')


    title: so.Mapped[int] = so.mapped_column(sa.String(200), nullable=False, default='', server_default='')
    body: so.Mapped[int] = so.mapped_column(sa.Text, nullable=False, default='', server_default='')
    dt_created: so.Mapped[DateTime] = so.mapped_column(sa.DateTime(timezone=True),
                                                       default=lambda: datetime.now(timezone.utc),
                                                       server_default=func.now())
    dt_updated: so.Mapped[DateTime] = so.mapped_column(sa.DateTime(timezone=True),
                                                       default=lambda: datetime.now(timezone.utc),
                                                       onupdate=lambda: datetime.now(timezone.utc))
    tags = relationship('Tag',
                        secondary=article_tag_association_table,
                        back_populates='articles',
                        )
    def __str__(self):
        return self.title
