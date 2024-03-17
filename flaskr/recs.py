from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api, user, match

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# similarity(): returns a similarity score and top shared artists/tracks (up to 10) between two users
# Parameters: user profile rows from the "users" table
# Returns: a number between 0 and 1 and two arrays

def similarity(user1, user2):
    # count how many items are identical in each category
    tracks1 = json.loads(user1[7])
    artists1 = json.loads(user1[8])
    tracks2 = json.loads(user2[7])
    artists2 = json.loads(user2[8])

    track_count = 0
    artist_count = 0
    track_weight = 0.5
    artist_weight = 0.5

    tracks = []
    artists = []

    for i in range(len(tracks1)):
        for j in range(len(tracks2)):
            if tracks1[i] == tracks2[j]:
                if track_count < 10:
                    tracks.append(tracks1[i])
                track_count = track_count + 1

    for i in range(len(artists1)):
        for j in range(len(artists2)):
            if artists1[i] == artists2[j]:
                if artist_count < 10:
                    artists.append(artists1[i])
                artist_count = artist_count + 1

    track_score = float(track_count) / float(len(tracks1))
    artist_score = float(artist_count) / float(len(artists1))

    if track_score > (1.2*artist_score):
        track_weight = 0.75
        artist_weight = 0.25
    elif artist_score > (1.2*track_score):
        track_weight = 0.25
        artist_weight = 0.75

    score = (track_weight*track_score)+(artist_weight*artist_score)

    return score, artists, tracks

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
        if match.is_available(id, row[1]):
            person["id"] = row[1]
            score = similarity(user_profile, row)
            person["score"] = score[0]
            person["artists"] = score[1]
            person["tracks"] = score[2]
            people.append(person)

    cursor.close()
    response["status"] = "ok"
    response["people"] = people

    return api.response(json.dumps(response))
