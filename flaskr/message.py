from flask import Flask, redirect, url_for, request
from datetime import datetime, timezone
import pymysql, spotipy, json, uuid
from flaskr import api, user, recs, match
from werkzeug.utils import secure_filename
from flaskr.initial_encrypt_generation import encrypt_data, generate_key, decrypt_data

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")
ec_db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes02", database="allvibes")#please change the details of the password and database
# send(): sends a message to a match
# HTTP POST parameters: current user's id, recepient id, and message contents
def get_key_for_id(id):
    ec_cr = ec_db.cursor()
    ec_cr.execute("SELECT key_value FROM key_table WHERE id = %s", (id,))
    result = ec_cr.fetchone()
    ec_cr.close()
    db.close()
    return result[0] if result else None

def send():
    id = request.form["from"]
    sender = user.get_internal_id(request.form["from"])
    recipient = request.form["to"]
    key=get_key_for_id(id)

    # before doing anything, we need to make sure these two users are matches
    response = {}
    if match.is_match(sender, recipient) is False:
        response["status"] = "fail - attempt to send message to non-match"
        return api.response(json.dumps(response))
    
    # generate a UUID for this message, to be used for reporting abusive behavior, etc
    id = uuid.uuid4()

    text = request.form["text"]
    text = encrypt_data(text,key)
    attachment = request.form["attachment"]
    attachment = encrypt_data(attachment,key)

    # here we at least know they're matches, so simply insert into the database
    now = datetime.now(timezone.utc)
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    cursor = db.cursor()
    count = cursor.execute("INSERT INTO messages (sender, recipient, id, seen, sent_time, encrypted_text, encrypted_attachment) VALUES ('" + sender + "', '" + recipient + "', '" + str(id) + "', false, '"+ date_string + "', '" + text + "', '" + attachment + "')")
    cursor.close()

    if count != 1:
        response["status"] = "fail - database error while sending message"
    else:
        db.commit()
        response["status"] = "ok"

    return api.response(json.dumps(response))

# receive(): receives UNREAD messages

def receive():
    id=request.args.get("from")
    sender = request.args.get("from")
    recipient = user.get_internal_id(request.args.get("id"))
    key=get_key_for_id(id)

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
        message["text"] = decrypt_data(row[6],key)
        message["attachment"] = decrypt_data(row[7],key)

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
        message["text"] = row[6]
        message["attachment"] = row[7]

        messages.append(message)
        final_count = final_count+1
    
    cursor.close()
    response["status"] = "ok"
    response["count"] = final_count

    if final_count < 20:
        response["last_page"] = True

    response["messages"] = messages
    
    return api.response(json.dumps(response))

# attach(): uploads a media attachment
# HTTP POST only - encoding type must be multipart/form-data
# Parameters:
# "id" of the current user
# "data" raw file data

def attach():
    id = user.get_internal_id(request.form["id"])
    data = request.files.get("data")
    file_id = uuid.uuid4()

    extension = data.filename.split(".")[-1].lower()

    filename = id + "-" + str(file_id) + "." + extension

    # TODO: uncomment this and comment the next line when we reach the deployment stage
    #data.save("../../allvibes-frontend/cdn/a/" + filename)
    data.save(filename)

    response = {}
    response["status"] = "ok"

    # TODO: likewise uncomment this and commejnt the next line when we reach the deployment stage
    #response["path"] = "/cdn/a/" + filename
    response["path"] = "/" + filename
    return api.response(json.dumps(response))
