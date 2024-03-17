from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# is_match(): checks if two given IDs are a match
# Parameters: both INTERNAL IDs
# Returns: boolean

def is_match(id1, id2):
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM matches WHERE (matched=true AND (id1='" + id1 + "' and id2='" + id2 + "') OR (id1='" + id2 + "' and id2='" + id1 + "'))")
    cursor.close()

    return count != 0

# is_available(): checks if an ID is available to be shown to another
# Parameters: both INTERNAL IDs
# Returns: Boolean

def is_available(id1, id2):
    cursor = db.cursor()

    # IMPORTANT: in this query, we're swapping id1 and id2 for a reason, do NOT touch this
    # the reasoning behind this is that we (id1) are the user looking for potential matches; so
    # this only counts if a possible other user (id2) swapped right on us
    # of course if the count returns zero then the user is automatically available to us
    #
    # tldr we're checking if ID2 is available to us, from the perspective of ID1
    count = cursor.execute("SELECT * FROM matches WHERE (matched=false AND unmatched=false AND id1='" + id2 + "' and id2='" + id1 + "')")
    cursor.close()

    return count <= 1

# attempt(): attempts to match with a user
# Parameters: HTTP POST - "me" (ID), "other" (ID), and "like" (0 = dislike, 1 = like)

def attempt():
    response = {}

    response["status"] = "ok"
    return api.response(json.dumps(response))
