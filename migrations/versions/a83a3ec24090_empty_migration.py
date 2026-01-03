"""empty migration

Revision ID: a83a3ec24090
Revises: a389ca14edf7
Create Date: 2025-12-31 20:21:42.469134

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from blog.models import User

# revision identifiers, used by Alembic.
revision = 'a83a3ec24090'
down_revision = 'a389ca14edf7'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind() # соединение с БД
    session = Session(bind=bind) # создаем сессию ORM
    if not session.query(User).filter_by(username='admin_migr').first():
        admin_migr = User(
            username='admin_migr',
            is_staff = True
        )
        session.add(admin_migr) # кладет объект в сессию
        session.commit() # создает новую строку в БД


def downgrade():
    bind = op.get_bind()  # соединение с БД
    session = Session(bind=bind)  # создаем сессию ORM
    session.query(User).filter_by(username='admin_migr').delete()
    session.commit()
