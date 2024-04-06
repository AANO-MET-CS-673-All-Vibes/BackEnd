from flask import Flask, redirect, url_for, request
import pymysql, json
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
