from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from app import helpers 


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    from app.routes import bp
    from app.errors import register_erros
    register_erros(app) 
    app.register_blueprint(bp)
    
    helpers.set_email_error_logging(app)
    helpers.set_file_logging(app)
        
        
    return app
