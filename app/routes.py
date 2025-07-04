from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit

from app.enums import HttpMethod
from app.forms import LoginForm, RegistrationForm
from app.models import User, AnonymousUser
from app import db

bp = Blueprint('main', __name__)


@bp.route('/', methods=[HttpMethod.GET])
@bp.route('/index', methods=[HttpMethod.GET])
@login_required
def index():
    args = {"title": "Greetings page",
            "user": {
                "is_authenticated": current_user.is_authenticated}}
    
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


@bp.route('/register', methods=[HttpMethod.GET, HttpMethod.POST])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        new_user = User(username=register_form.username.data,
                        email = register_form.email.data)
        new_user.set_password(register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    args = {"title": "Registration Page",
            "user": {
                "is_authenticated": current_user.is_authenticated}}
    return render_template("register.html", form=register_form, args=args)

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
        login_user(user=user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=login_form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route("/secret", methods=[HttpMethod.GET])
def secret():
    return render_template("secret.html")

