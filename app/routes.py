from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa

from app.enums import HttpMethod
from app.forms import LoginForm
from app.models import User, AnonymousUser
from app import db

bp = Blueprint('main', __name__)


@bp.route('/', methods=[HttpMethod.GET])
@bp.route('/index', methods=[HttpMethod.GET])
def index():
    if current_user.is_authenticated:
        session_user = User.load_user(current_user.get_id())
    else:
        session_user = AnonymousUser()
    print(session_user)
    args = {"title": "Greetings page",
            "user": {
                "is_authenticated": current_user.is_authenticated,
                "username": session_user.username}}
    
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            "author": {'username': "Gregory"},
            'body': 'New AI agent make people too anxient! How\'s it going?'
        }
    ]
    return render_template("index.html", args = args, posts=posts)

@bp.route("/login", methods=[HttpMethod.GET, HttpMethod.POST])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == login_form.username.data))
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('main.login'))
        login_user(
            user,
            remember=login_form.remember_me.data
            )
        return redirect(url_for('main.index'))
    return render_template("login.html", title="Sign in", form=login_form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route("/secret", methods=[HttpMethod.GET])
def secret():
    return render_template("secret.html")

