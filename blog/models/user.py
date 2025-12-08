from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from .database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True, nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.String(30), default='no name')
    is_staff: so.Mapped[bool] = so.mapped_column(nullable=False, default=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'<User #{self.id}:{self.username}'
