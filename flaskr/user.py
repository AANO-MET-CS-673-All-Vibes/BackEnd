from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# userinfo: retrieves user info; ID is specified as a GET parameter

def userinfo():
    id = request.args.get("id")

    response = {}

    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM user WHERE id=\"" + id + "\"")
    if count == 0:
        cursor.close()
        response["status"] = "fail"
        return api.response(json.dumps(response))
    
    row = cursor.fetchone()
    response["status"] = "ok"
    response["id"] = id
    response["name"] = row[2]
    response["gender"] = row[3]
    response["dob"] = str(row[4])
    response["bio"] = row[5]
    response["image"] = row[6]
    response["top_tracks"] = row[7]     # TODO: ONLY TOP 10
    response["top_artists"] = row[8]    # TODO: ONLY TOP 5
    response["last_online"] = row[10]

    return api.response(json.dumps(response))
