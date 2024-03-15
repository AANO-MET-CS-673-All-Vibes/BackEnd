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

    if row[7] is not None:
        response["top_tracks"] = json.loads(row[7])     # TODO: ONLY TOP 10
    else:
        response["top_tracks"] = []
    
    if row[8] is not None:
        response["top_artists"] = json.loads(row[8])    # TODO: ONLY TOP 5
    else:
        response["top_artists"] = []
    response["last_online"] = row[10]

    return api.response(json.dumps(response))

# update: this updates the user's top tracks/artists
def update():
    sp = spotipy.Spotify(auth=request.form["token"])
    
    raw_top_tracks = sp.current_user_top_tracks(limit=50, offset=0, time_range="medium_term")
    raw_top_artists = sp.current_user_top_artists(limit=25, offset=0, time_range="medium_term")

    # now we filter out all the unnecessary metadata
    # for tracks we only need track name and artist name; for artists we only need their name, photo, and genre
    top_tracks = []
    
    for raw_track in raw_top_tracks["items"]:
        track = {}
        track["name"] = raw_track["name"]
        track["artist"] = raw_track["artists"][0]["name"]
        top_tracks.append(track)

    top_artists = []

    for raw_artist in raw_top_artists["items"]:
        artist = {}
        artist["name"] = raw_artist["name"]
        artist["genre"] = raw_artist["genres"]
        artist["image"] = raw_artist["images"][0]["url"]
        top_artists.append(artist)

    # now convert both to JSON
    tracks_json = json.dumps(top_tracks).replace("'", "\\'")
    artists_json = json.dumps(top_artists).replace("'", "\\'")

    # and update the database
    cursor = db.cursor()
    cursor.execute("UPDATE user SET top_tracks='" + tracks_json + "' WHERE id='" + request.form["id"] + "'")
    cursor.execute("UPDATE user SET top_artists='" + artists_json + "' WHERE id='" + request.form["id"] + "'")
    cursor.close()
    db.commit()

    response = {}
    response["status"] = "ok"
    return api.response(json.dumps(response))
