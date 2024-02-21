import os

from flask import Flask
from flaskr import login

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    # build all routings

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/login')
    def route_login():
        return login.login()

    return app
