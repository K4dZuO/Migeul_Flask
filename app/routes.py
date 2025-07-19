from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from datetime import datetime, timezone
from urllib.parse import urlsplit

from app.enums import HttpMethod
from app.forms import LoginForm, RegistrationForm, EditProfileForm, FollowForm
from app.models import User, Post, Comment
from app import db


bp = Blueprint('main', __name__)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route('/', methods=[HttpMethod.GET])
@bp.route('/index', methods=[HttpMethod.GET])
@login_required
def index():
    posts = db.session.scalars(sa.select(Post).order_by(sa.desc(Post.added_at))).all()
    return render_template("index.html", title = "Home", posts=posts)


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
    return render_template("register.html", form=register_form, title="Registration page")


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


@bp.route('/edit_profile', methods=[HttpMethod.GET, HttpMethod.POST])
@login_required
def edit_profile():
    profile_form = EditProfileForm(original_username = current_user.username)
    if profile_form.validate_on_submit():
        current_user.username = profile_form.username.data
        current_user.about = profile_form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user_profile', username=current_user.username))
    elif request.method == HttpMethod.GET:
        profile_form.username.data = current_user.username
        profile_form.about.data = current_user.about
    return render_template("edit_profile.html", title="Edit Profile", form = profile_form)


@bp.route('/follow/<username>', methods=[HttpMethod.POST])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user_profile', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('main.user_profile', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=[HttpMethod.POST])
@login_required
def unfollow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user_profile', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('main.user_profile', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/user/<username>')
@login_required
def user_profile(username):
    follow_form = FollowForm()
    asked_user = db.first_or_404(sa.select(User).where(User.username==username))
    if asked_user:
        posts = db.session.scalars(sa.select(Post).where(Post.user_id == asked_user.id)).all()
        comments = db.session.scalars(sa.select(Comment).where(Comment.user_id == asked_user.id)).all()
    else:
        posts = None
        comments = None
        
    args = {
        "raw_username": username,
        "user": asked_user,
        "posts": posts,
        "comments": comments,
        "follow_form": follow_form
        }
    return render_template('user.html', title="User Page", **args)


@bp.route("/secret", methods=[HttpMethod.GET])
def secret():
    return render_template("secret.html")
