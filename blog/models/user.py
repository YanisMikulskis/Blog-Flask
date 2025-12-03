from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin
from .database import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(30), default='Not Name')
    is_staff = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User #{self.id}:{self.username}'



