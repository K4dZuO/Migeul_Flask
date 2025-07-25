from better_profanity import profanity
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import os
from flask import Flask

from config import Config


def check_profanity(text: str) -> bool:
    return profanity.contains_profanity(text)


def set_email_error_logging(app: Flask):
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], 
                subject='Microblog Failure',
                credentials=auth, 
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

def set_file_logging(app: Flask):
    if not os.path.exists(Config.LOG_FOLDER):
        os.mkdir(Config.LOG_FOLDER)
    file_handler = RotatingFileHandler(f'{Config.LOG_FOLDER}/microblog.log', maxBytes=10240,
                                    backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
