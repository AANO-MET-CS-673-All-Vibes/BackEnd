import os

from flask import Flask
from flaskr import login, account, user, recs, match

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
    
    @app.route("/weblogin")
    def route_weblogin():
        return login.weblogin()

    @app.route('/callback')
    def route_callback():
        return login.callback()

    #@app.route('/operations')
    #def route_operations():
    #    return login.operations()

    @app.route("/create", methods=["POST"])
    def route_create():
        return account.create()
    
    @app.route("/websignup", methods=["POST"])
    def route_websignup():
        return account.websignup()

    @app.route("/userinfo")
    def route_userinfo():
        return user.userinfo()
    
    @app.route("/update", methods=["POST"])
    def route_update():
        return user.update()
    
    @app.route("/recs")
    def route_recs():
        return recs.recs()
    
    @app.route("/attempt", methods=["POST"])
    def route_attempt():
        return match.attempt()

    return app

