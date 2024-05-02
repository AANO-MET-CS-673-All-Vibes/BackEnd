from flask import Flask, redirect, url_for, request
from datetime import datetime, timezone
import pymysql, spotipy, uuid, json
from flaskr import login, api, input_validation
from flaskr.initial_encrypt_generation import encrypt_data, generate_key, decrypt_data

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")
ec_db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes02", database="allvibes")#please change the details of the password and database

# TO AMRUTHA: FEEL FREE TO REWRITE ALL OF THE DATABASE INTERACTIONS AS YOU SEE FIT
# in this prototype architecture, we just depend on a MySQL table called "accounts"
# the columns in this table rn are name and email, but will someday include gender,
# sexuality, bio, profile pic, top tracks/artists, etc

# exists(): this method determines if an account exists or not
# Parameter: email - email associated with this account
# Return: Boolean
 
def exists(email):
    cursor = ec_db.cursor()
    
    count = cursor.execute("SELECT * FROM accounts WHERE email=\"" + email + "\"")

    cursor.close()

    if count == 0:
        return False
    else:
        return True
    
# email_to_id(): returns the UUID associated with an email
    
def email_to_id(email):
    cursor = ec_db.cursor()
    count = cursor.execute("SELECT * FROM accounts WHERE email=\"" + email + "\"")
    
    if count == 0:
        return None
    
    row = cursor.fetchone()
    cursor.close()
    return row[0]

# create(): creates a new account

def create():
    response = {}

    # input validation
    if not input_validation.validate_name(request.form["name"]):
        response["status"] = "fail"
        return api.response(json.dumps(response))

    id = uuid.uuid4()           # first generate a UUID
    internal_id = uuid.uuid4()  # for security
    key = generate_key()

    # account creation date
    now = datetime.now(timezone.utc)
    date_string = now.strftime("%Y-%m-%d")
    email = request.form["email"]
    enc_email = encrypt_data(email,key)


    ec_cur = ec_db.cursor()
    # now add to the initial accounts table
    cursor = db.cursor()
    rows = cursor.execute("INSERT INTO accounts ( id, encrypted_email, created ) VALUES ( \"" + str(id) + "\", \"" + enc_email + "\", \"" + date_string + "\" )")
    rows2 = ec_cur.execute("INSERT INTO key_table ( id, email, key_value ) VALUES ( \"" + str(id) + "\", \"" + email + "\", \"" + key + "\" )")

    if rows != 1:
        response["status"] = "fail"
        return api.response(json.dumps(response))
    if rows2 != 1:
        response["status"] = "fail"
        return api.response(json.dumps(response))

    # now to the user table
    name=request.form["name"]
    enc_name = encrypt_data(name,key)
    gender=request.form["gender"]
    enc_gender = encrypt_data(gender,key)
    dob=request.form["dob"]
    enc_dob = encrypt_data(dob,key)
    rows = cursor.execute("INSERT INTO users ( id, internal_id, encrypted_name, encrypted_gender, encrypted_dob, like_count ) VALUES ( \"" + str(id) + "\", \"" + str(internal_id) + "\", \"" + enc_name + "\", \"" + enc_gender + "\", \"" + enc_dob + "\", \"0\" )")

    if rows != 1:
        response["status"] = "fail"
        return api.response(json.dumps(response))

    cursor.close()
    ec_cur.close()
    db.commit()
    ec_db.commit()

    response["status"] = "ok"
    response["id"] = str(id)
    response["token"] = request.form["token"]
    return api.response(json.dumps(response))

def websignup():
    # creating a new account
    output = create()
    output = json.loads(str(output[0]))

    return redirect("https://allvibes.jewelcodes.io/profile.html?id=" + output["id"] + "&token=" + output["token"])

