import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or ('sqlite:///' + os.path.join(basedir, 'app.db'))
    SOURCE_FOLDER=os.environ['SOURCE_FOLDER']
    USERS_AVATARS=os.environ['USERS_AVATARS']
    LOG_FOLDER=os.environ['LOG_FOLDER']

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['erschofogt@gmail.com']

    POSTS_PER_PAGE=int(os.environ['POSTS_PER_PAGE'])
