import sqlalchemy as sa
import sqlalchemy.orm as so
from os import path

from config import Config
from app.models import User, Post
from app import db, create_app

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

def create_db(app):
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if not path.exists(Config.SQLALCHEMY_DATABASE_URI):
    create_db(app)
    