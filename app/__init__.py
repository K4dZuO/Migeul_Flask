from flask import Flask


app = Flask(__name__)
from app.routers import base 


def run_app():
    app.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    run_app()
