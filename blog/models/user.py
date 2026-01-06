from typing import Optional
from xmlrpc.client import Binary

import sqlalchemy as sa
import sqlalchemy.orm as so
from blog.extension import db
from flask_login import UserMixin
from flask_bcrypt import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True, nullable=False)

    name: so.Mapped[str] = so.mapped_column(sa.String(30), nullable=False, default='no name', server_default='no name')

    last_name: so.Mapped[str] = so.mapped_column(sa.String(50),
                                                 unique=False,
                                                 nullable=False,
                                                 default='',
                                                 server_default='')

    email: so.Mapped[str] = so.mapped_column(sa.String(50),
                                             unique=True,
                                             nullable=True,
                                   )

    is_staff: so.Mapped[bool] = so.mapped_column(nullable=False, default=False, server_default=sa.false())
    _password: so.Mapped[bytes] = so.mapped_column(sa.LargeBinary, nullable=True)


    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        if len(value) < 8:
            raise ValueError(f'Пароль должен быть не менее 8 символов!')

        self._password = generate_password_hash(value)


    def validate_password(self, password) -> bool:
        return check_password_hash(self._password, password)

    def __repr__(self):
        return f'<User #{self.id}:{self.username}'
