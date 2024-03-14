import os

from flask import Flask
from flaskr import login, account

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/login')
    def route_login():
        return login.login()

    @app.route('/callback')
    def route_callback():
        return login.callback()

    #@app.route('/operations')
    #def route_operations():
    #    return login.operations()

    @app.route("/create", methods=["GET", "POST"])
    def route_create():
        return account.create()

    @app.route("/home")
    def route_home():
        return "<h1>Placeholder for the home page! For now, this just means we know this account alr exists</h1>"

    return app
