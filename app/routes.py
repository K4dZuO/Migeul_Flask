from flask import render_template, redirect, flash, url_for

from app.enums import HttpMethod
from app import app
from app.forms import LoginForm

@app.route('/', methods=[HttpMethod.GET])
@app.route('/index', methods=[HttpMethod.GET])
def index():
    args = {"name": "Maxim",
            "title": "Greetings page",
            "add_info" : {
                "color_eyes": "green",
                "color_hair": "blond"
            }
        }
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

@app.route("/login", methods=[HttpMethod.GET, HttpMethod.POST])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash(f"Login requested: {login_form.username.data}")
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign in", form=login_form)

@app.route("/secret", methods=[HttpMethod.GET])
def secret():
    return render_template("secret.html")

