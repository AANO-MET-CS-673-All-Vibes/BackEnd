from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api, user, recs

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# is_match(): checks if two given IDs are a match
# Parameters: both INTERNAL IDs
# Returns: boolean

def is_match(id1, id2):
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM matches WHERE (matched=true AND unmatched=false AND ((id1='" + id1 + "' and id2='" + id2 + "') OR (id1='" + id2 + "' and id2='" + id1 + "')))")
    cursor.close()

    return count != 0

# is_unmatch(): checks if two given IDs unmatched
# Parameters: both INTERNAL IDs
# Returns: boolean

def is_unmatch(id1, id2):
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM matches WHERE (matched=true AND unmatched=true AND ((id1='" + id1 + "' and id2='" + id2 + "') OR (id1='" + id2 + "' and id2='" + id1 + "')))")
    cursor.close()

    return count != 0

# is_available(): checks if an ID is available to be shown to another
# Parameters: both INTERNAL IDs
# Returns: Boolean

def is_available(id1, id2):
    # obviously unavailable if we already matched
    if is_match(id1, id2) or is_unmatch(id1, id2):
        return False

    cursor = db.cursor()

    # did we already swipe on this user?
    count = cursor.execute("SELECT * FROM matches WHERE (id1='" + id1 + "' AND id2='" + id2 + "')")
    if count != 0:
        cursor.close()
        return False
    
    # has the other user swiped on us and possibly unmatched?
    # note the intentional ID swap
    count = cursor.execute("SELECT * FROM matches WHERE (unmatched=true) AND (id1='" + id2 + "' AND id2='" + id1 + "')")
    cursor.close()
    if count != 0:
        return False

    return True

# attempt(): attempts to match with a user
# Parameters: HTTP POST - "me" (ID), "other" (ID), and "like" (0 = dislike, 1 = like)

def attempt():
    response = {}
    response["status"] = "ok"

    me = user.get_internal_id(request.form["me"])
    other = request.form["other"]
    like_post = request.form["like"]

    # 0 = dislike, 1 or anything else = like
    like = (int(like_post) >= 1)

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # first check if the other user has already swiped; this means checking if ID1 == other and ID2 == me
    # if not, then we will insert our own new row
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM matches WHERE (matched=false AND unmatched=false) AND (id1='" + other + "' AND id2='" + me + "')")

    if count != 0:
        # here we have potential to make a match!
        if like:
            # match!
            # come up with match time
            count = cursor.execute("UPDATE matches SET matched=true,match_time='" + date_string + "' WHERE (id1='" + other + "' AND id2='" + me + "')")
        else:
            # not a match :(
            count = cursor.execute("UPDATE matches SET matched=true,unmatched=true WHERE (id1='" + other + "' AND id2='" + me + "')")

        if count != 1:
            cursor.close()
            response["status"] = "fail"
            return api.response(json.dumps(response))
        else:
            response["matched"] = like
    else:
        # ok not a match, but rather a first move - this may be a like or a dislike
        response["matched"] = False
        if like:
            count = cursor.execute("INSERT INTO matches (id1, id2, matched, unmatched, attempt_time) VALUES ('" + me + "', '" + other + "', false, false, '" + date_string + "')")
        else:
            count = cursor.execute("INSERT INTO matches (id1, id2, matched, unmatched, attempt_time) VALUES ('" + me + "', '" + other + "', false, true, '" + date_string + "')")
        
        if count != 1:
            cursor.close()
            response["status"] = "fail"
            return api.response(json.dumps(response))

    cursor.close()
    db.commit()
    return api.response(json.dumps(response))

# matches(): returns a list of this user's matches

def matches():
    id = user.get_internal_id(request.args.get("id"))
    response = {}
    people = []

    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM matches WHERE (matched=true AND unmatched=false) AND (id1='" + id + "' OR id2='" + id + "')")
    if count == 0:
        cursor.close()
        response["status"] = "ok"
        response["people"] = people
        return api.response(json.dumps(response))

    for i in range(count):
        person = {}
        row = cursor.fetchone()

        if row[0] == id:
            person["id"] = row[1]
        else:
            person["id"] = row[0]

        me = user.get_profile(id)
        other = user.get_profile(person["id"])

        score = recs.similarity(me, other)
        person["score"] = score[0]
        person["artists"] = score[1]
        person["tracks"] = score[2]

        people.append(person)

    cursor.close()
    response["status"] = "ok"
    response["people"] = people

    return api.response(json.dumps(response))

# unmatch(): removes a match
# HTTP POST parameters: "me" and "other"

def unmatch():
    response = {}

    me = user.get_internal_id(request.form["me"])
    other = request.form["other"]

    # unmatch time
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # update the match table
    cursor = db.cursor()
    count = cursor.execute("UPDATE matches SET unmatched=true,unmatch_time='" + date_string + "' WHERE (id1='" + me + "' AND id2='" + other + "') OR (id1='" + other + "' AND id2='" + me + "')")
    cursor.close()

    if count != 1:
        response["status"] = "fail"
        return api.response(json.dumps(response))
    
    response["status"] = "ok"
    return api.response(json.dumps(response))
