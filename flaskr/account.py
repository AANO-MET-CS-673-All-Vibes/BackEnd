from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, uuid, json
from flaskr import login, api

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# TO AMRUTHA: FEEL FREE TO REWRITE ALL OF THE DATABASE INTERACTIONS AS YOU SEE FIT
# in this prototype architecture, we just depend on a MySQL table called "accounts"
# the columns in this table rn are name and email, but will someday include gender,
# sexuality, bio, profile pic, top tracks/artists, etc

# exists(): this method determines if an account exists or not
# Parameter: email - email associated with this account
# Return: Boolean
 
def exists(email):
    cursor = db.cursor()
    
    count = cursor.execute("SELECT * FROM account WHERE email=\"" + email + "\"")

    cursor.close()

    if count == 0:
        return False
    else:
        return True
    
# email_to_id(): returns the UUID associated with an email
    
def email_to_id(email):
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM account WHERE email=\"" + email + "\"")
    
    if count == 0:
        return None
    
    row = cursor.fetchone()
    cursor.close()
    return row[0]

# create(): creates a new account

def create():
    response = {}

    id = uuid.uuid4()           # first generate a UUID
    internal_id = uuid.uuid4()  # for security

    # account creation date
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    # now add to the initial accounts table
    cursor = db.cursor()
    rows = cursor.execute("INSERT INTO account ( id, email, created ) VALUES ( \"" + str(id) + "\", \"" + request.form["email"] + "\", \"" + date_string + "\" )")

    if rows != 1:
        response["status"] = "fail"
        return api.response(json.dumps(response))

    # now to the user table
    rows = cursor.execute("INSERT INTO user ( id, internal_id, name, gender, dob, like_count ) VALUES ( \"" + str(id) + "\", \"" + str(internal_id) + "\", \"" + request.form["name"] + "\", \"" + request.form["gender"] + "\", \"" + request.form["dob"] + "\", \"0\" )")

    if rows != 1:
        response["status"] = "fail"
        return api.response(json.dumps(response))

    cursor.close()
    db.commit()

    response["status"] = "ok"
    response["id"] = str(id)
    return api.response(json.dumps(response))

def websignup():
    # creating a new account
    output = create()
    output = json.loads(str(output[0]))

    return redirect("http://127.0.0.1:8080/home?id=" + output["id"])

