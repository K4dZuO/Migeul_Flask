from flask import current_app, request, g

from app.enums import HttpMethod
from app import app


@app.route("/", methods=[HttpMethod.GET])
def index():
    return "Hello, dear friend!", 200

@app.route("/greet", methods=[HttpMethod.GET])
def common_greet():
    print(current_app.name)
    return "It's ordinary greetings for everyone who got here!"

@app.route("/greet/<name>", methods=[HttpMethod.GET])
def name_greet(name):
    return f"Look at who came here! It's {name} by self!"

@app.route("/sum/<int:num1>/<int:num2>", methods=[HttpMethod.GET])
def operator_test(num1, num2):
    return f"{num1}+{num2}+{num1+num2}"

@app.route("/handle", methods=[HttpMethod.GET])
def handle_params():
    name = request.args.get("name")
    return name

@app.route('/<lang_code>/about')
def about(lang_code):
    g.lang_code = lang_code
    return g.lang_code


def show_user_func(name, surname):
    return f"I see you, {name} {surname}."

app.add_url_rule(rule="/show_user/<name>/<surname>", endpoint="show_user", view_func=show_user_func)
