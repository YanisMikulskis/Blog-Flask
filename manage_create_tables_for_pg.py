from blog.extension import db
from blog.app import create_app

app = create_app()

with app.app_context():
    db.create_all()
    print(f'all tables creates for postgres or already exists')