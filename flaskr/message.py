from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json, uuid
from flaskr import api, user, recs, match

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# send(): sends a message to a match
# HTTP POST parameters: current user's id, recepient id, and message contents

def send():
    sender = user.get_internal_id(request.form["from"])
    recipient = request.form["to"]

    # before doing anything, we need to make sure these two users are matches
    response = {}
    if match.is_match(sender, recipient) is False:
        response["status"] = "fail - attempt to send message to non-match"
        return api.response(json.dumps(response))
    
    # generate a UUID for this message, to be used for reporting abusive behavior, etc
    id = uuid.uuid4()

    text = request.form["text"]
    attachment = request.form["attachment"]

    # here we at least know they're matches, so simply insert into the database
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    cursor = db.cursor()
    count = cursor.execute("INSERT INTO messages (sender, recipient, id, seen, sent_time, text, attachment) VALUES ('" + sender + "', '" + recipient + "', '" + id + "', false, '"+ date_string + "', '" + text + "', '" + attachment + "')")
    cursor.close()

    if count != 1:
        response["status"] = "fail - database error while sending message"
    else:
        db.commit()
        response["status"] = "ok"

    return api.response(json.dumps(response))

# receive(): receives UNREAD messages

def receive():
    sender = request.args.get("from")
    recipient = user.get_internal_id(request.args.get("id"))

    response = {}
    if match.is_match(sender, recipient) is False:
        response["status"] = "fail - attempt to receive messages from non-match"
        return api.response(json.dumps(response))

    # pull from the database
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM messages WHERE (sender='" + sender + "' AND recipient='" + recipient + "' AND seen=false) ORDER BY sent_time DESC")
    
    messages = []

    for i in range(count):
        message = {}
        row = cursor.fetchone()

        message["from"] = sender
        message["to"] = request.args.get("id")
        message["id"] = row[3]
        message["timestamp"] = str(row[4])
        message["text"] = row[5]
        message["attachment"] = row[6]

        messages.append(message)
    
    cursor.close()
    response["status"] = "ok"
    response["messages"] = messages
    return api.response(json.dumps(response))

# history(): retrieves message history
# GET parameters: "id" and "context" and "page"

def history():
    me = user.get_internal_id(request.args.get("id"))
    context = request.args.get("context")
    page = int(request.args.get("page"))

    response = {}
    if match.is_match(me, context) is False:
        response["status"] = "fail - attempt to retrieve message history with non-match"
        return api.response(json.dumps(response))
    
    # pull from the database
    cursor = db.cursor()
    count = cursor.execute("SELECT * FROM messages WHERE (sender='" + me + "' AND recipient='" + context + "') OR (sender='" + context + "' AND recipient='" + me + "') ORDER BY sent_time DESC")

    if count < (page*20):
        cursor.close()
        response["status"] = "ok"
        response["count"] = 0
        response["last_page"] = True
        response["messages"] = []
        return api.response(json.dumps(response))

    messages = []
    final_count = 0

    # keep going until we reach our desired page
    for i in range(page*20):
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            response["status"] = "ok"
            response["count"] = 0
            response["last_page"] = True
            response["messages"] = []
            return api.response(json.dumps(response))

    for i in range(count):
        message = {}
        row = cursor.fetchone()

        if row[0] == me:
            message["form"] = request.args.get("id")
        else:
            message["from"] = row[0]

        if row[1] == me:
            message["to"] = request.args.get("id")
        else:
            message["to"] = row[1]
        
        message["id"] = row[3]
        message["timestamp"] = str(row[4])
        message["text"] = row[5]
        message["attachment"] = row[6]

        messages.append(message)
        final_count = final_count+1
    
    cursor.close()
    response["status"] = "ok"
    response["count"] = final_count

    if final_count < 20:
        response["last_page"] = True

    response["messages"] = messages
    
    return api.response(json.dumps(response))