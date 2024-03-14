from flask import Flask, redirect, request
import spotipy, json
from spotipy.oauth2 import SpotifyOAuth
from flaskr import account

# Spotify API credentials
SPOTIFY_CLIENT_ID = '710ea14ca1d949bda4e072ff4a4ebd21'
SPOTIFY_CLIENT_SECRET = '0ff7573b7c0f4c7eaa987b983f81df84'
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'  # TODO: Update with your redirect URI so that we can login via spotify as we discussed and not with google account and then connect the spotify account with it, Though i think we should keep the login via google and then connect the music apps account in the app itself(browser version) it is kind of a standard way if we are going to give support for spotify and apple music. See what you think NOUR
#SCOPE = 'user-library-read'  # TODO: For example scope i am asking to get the library of the user you can change it as you want NOUR.
SCOPE = "user-top-read,user-read-email,user-read-private"     # i figured medium-term top songs are a better way to judge rather than liked songs that can accumulate songs from years ago you no longer like (?)

def login():
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def callback():
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE)
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    token = token_info["access_token"]
    
    if not token_info:
        return redirect("/login")

    sp = spotipy.Spotify(auth=token)
    profile = sp.me()

    output = {}
    output["status"] = "ok"
    output["token"] = token

    # check if this account exists from the email
    if account.exists(profile["email"]):
        output["exists"] = True
    else:
        output["exists"] = False

    return json.dumps(output)
