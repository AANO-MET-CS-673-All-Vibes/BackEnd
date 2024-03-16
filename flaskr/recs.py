from flask import Flask, redirect, url_for, request
from datetime import datetime
import pymysql, spotipy, json
from flaskr import api

db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")

# recs(): returns a list of recommendations to "swipe" on, each with a similarity score

def recs():
    response = {}
    people = []

    response["status"] = "ok"

    return api.response(json.dumps(response))
