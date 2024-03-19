from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api, user, recs, match

# send(): sends a message to a match
# HTTP POST parameters: current user's id, recepient id, and message contents

def send():
    # PLACEHOLDER
    response = {}
    response["status"] = "ok"

    return api.response(json.dumps(response))

# receive(): receives UNREAD messages

def receive():
    # PLACEHOLDER
    response = {}
    response["status"] = "ok"

    return api.response(json.dumps(response))

# history(): retrieves message hisotory

def history():
    # PLACEHOLDER
    response = {}
    response["status"] = "ok"

    return api.response(json.dumps(response))