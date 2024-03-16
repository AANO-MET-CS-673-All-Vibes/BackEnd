from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api, user, match

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# score(): returns a similarity score between two users' music taste
# Parameters: rows from the "users" table
# Returns: a number between 0 and 1

def score(user1, user2):
    return 0.37     # test

# recs(): returns a list of recommendations to "swipe" on, each with a similarity score
# This is essentially the core of the entire app

def recs():
    response = {}
    people = []

    id = user.get_internal_id(request.args.get("id"))
    user_profile = user.get_profile(id)

    # pull people from the main user database, and then recommend the ones that aren't matches
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM users WHERE internal_id!='" + id + "'")
    if count == 0:
        cursor.close()
        response["status"] = "ok"
        response["people"] = []
        return api.response(json.dumps(response))

    # now we can go through them one by one, only adding people that aren't already matches
    for i in range(count):
        person = {}
        row = cursor.fetchone()
        if match.is_match(id, row[1]) == False:
            person["id"] = row[1]
            person["score"] = score(user_profile, row)

        people.append(person)

    cursor.close()
    response["status"] = "ok"
    response["people"] = people

    return api.response(json.dumps(response))
