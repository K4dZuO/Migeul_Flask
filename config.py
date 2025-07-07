import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or ('sqlite:///' + os.path.join(basedir, 'app.db'))
    SOURCE_FOLDER=os.environ['SOURCE_FOLDER']
    USERS_AVATARS=os.environ['USERS_AVATARS']
