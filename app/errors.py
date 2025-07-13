from flask import render_template, Flask

from app import db


def not_found_error(error):
    return render_template('404.html'), 404


def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

def register_erros(app: Flask):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
