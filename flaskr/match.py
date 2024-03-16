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
    count = cursor.execute("SELECT * FROM match WHERE (id1='" + id1 + "' and id2='" + id2 + "') OR (id1='" + id2 + "' and id2='" + id1 + "')")
    cursor.close()

    return count != 0
