from flask import Flask, redirect, url_for, request
import pymysql, json, uuid
from flaskr import api

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# bio(): /edit/bio endpoint edits the bio of the user
# HTTP POST parameters: id and bio

def bio():
    id = request.form["id"]
    bio = request.form["bio"]

    response = {}

    cursor = db.cursor()
    count = cursor.execute("UPDATE users SET bio='" + bio + "' WHERE id='" + id + "'")
    cursor.close()

    if count != 1:
        response["status"] = "fail - could not update database"
    else:
        db.commit()
        response["status"] = "ok"

    return api.response(json.dumps(response))

# pfp(): /edit/pfp endpoint uploads a new profile picture
# HTTP POST parameters: id and data containing raw file data

def pfp():
    response = {}
    id = request.form["id"]
    data = request.files.get("data")
    file_id = uuid.uuid4()

    extension = data.filename.split(".")[-1].lower()

    filename = id + "-" + str(file_id) + "." + extension

    # TODO: uncomment this and comment the next line when we reach the deployment stage
    #data.save("../../allvibes-frontend/cdn/a/" + filename)
    data.save("flaskr/static/" + filename)

    # now update the database
    cursor = db.cursor()
    cursor.execute("UPDATE users SET image='/static/" + filename + "' WHERE id='" + id + "'")
    cursor.close()
    db.commit()

    if cursor == 1:
        response["status"] = "ok"
    else:
        response["status"] = "fail - unable to update database"

    return api.response(json.dumps(response))
