import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .user import User
from blog.extension import db


class Author(db.Model):
    __tablename__ = 'authors'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), unique=True, nullable=False)
    user = relationship('User', back_populates='author') #back_populates - указание на поле author в модели User
    articles = relationship('Article', back_populates='author')
    def __repr__(self):
        user_name = User.query.filter_by(id=self.user_id).one_or_none()
        return (f'Статья Автора {self.id} на Юзере'
                f' {self.user_id}, он же {user_name}')