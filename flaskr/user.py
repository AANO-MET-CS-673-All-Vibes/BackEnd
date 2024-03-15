from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

UPDATE_THRESHOLD        = 604800    # update top tracks/artists every week; reasonable when we're 6-month averages

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
    response = {}

    # check if we even need to update at all
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM user WHERE id='" + request.form["id"] + "'")
    if count != 1:
        response["status"] = "fail"
        return api.response(json.dumps(response))
    
    row = cursor.fetchone()

    last_updated = row[9]
    now = datetime.now().date()
    #print("last updated: " + str(last_updated))

    diff = now-last_updated

    # only update if a certain duration has passed since the last update
    if last_updated is not None and diff.total_seconds() < UPDATE_THRESHOLD:
        response["status"] = "ok"
        response["updated"] = False
        return api.response(json.dumps(response))

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
    cursor.execute("UPDATE user SET top_tracks='" + tracks_json + "' WHERE id='" + request.form["id"] + "'")
    cursor.execute("UPDATE user SET top_artists='" + artists_json + "' WHERE id='" + request.form["id"] + "'")

    # current time
    date_string = now.strftime("%Y-%m-%d")

    cursor.execute("UPDATE user SET last_updated=\"" + date_string + "\" WHERE id='" + request.form["id"] + "'")

    cursor.close()
    db.commit()

    response["status"] = "ok"
    response["updated"] = True
    return api.response(json.dumps(response))
