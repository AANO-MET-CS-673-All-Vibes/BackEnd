from flask import Flask, redirect, url_for, request, session
import pymysql, spotipy

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# exists(): this method determines if an account exists or not
# Parameter: email - email associated with this account
# Return: Boolean

def exists(email):
    cursor = db.cursor()
    
    count = cursor.execute("SELECT * FROM accounts WHERE email=\"" + email + "\"")

    cursor.close()

    if count == 0:
        return False
    else:
        return True

def create():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect('/login')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    profile = sp.me()

    if request.method == 'POST':
        # HTTP POST request
        # here we're saving the user's submitted form into the database
        cursor = db.cursor()

        rows = cursor.execute("INSERT INTO accounts ( name, email ) VALUES ( \"" + request.form["name"] + "\", \"" + profile["email"] + "\" )")
        if rows != 1:
            return "<h1>Unable to create account</h1>"  # TODO: obviously a nicer error page someday
        
        db.commit()
        cursor.close()
        
        return "<h1>Created a new account</h1>"

    else:
        # HTTP GET request
        # here we present the user with a form that allows them to type in their name, birthday, etc
        return redirect(url_for("static", filename="create.html"))  # TODO: temporary just so i can get this done!!! this will be replaced with the actual frontend
