from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    
    from app import models
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    
    with app.app_context():
        if not sa.inspect(db.engine).has_table(db.engine, 'users'):
            print("There's no any table")
        else:
            print("Yes, I see the table.")
    
    return app
