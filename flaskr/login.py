from flask import Flask, redirect, request
import spotipy, json
from spotipy.oauth2 import SpotifyOAuth
from flaskr import api, account

# Spotify API credentials
SPOTIFY_CLIENT_ID = '710ea14ca1d949bda4e072ff4a4ebd21'
SPOTIFY_CLIENT_SECRET = '0ff7573b7c0f4c7eaa987b983f81df84'
SPOTIFY_REDIRECT_URI = 'https://allvibes.jewelcodes.io/api/callback'  # TODO: Update with your redirect URI so that we can login via spotify as we discussed and not with google account and then connect the spotify account with it, Though i think we should keep the login via google and then connect the music apps account in the app itself(browser version) it is kind of a standard way if we are going to give support for spotify and apple music. See what you think NOUR
SPOTIFY_REDIRECT_WEB_URI = "https://allvibes.jewelcodes.io/callback"
#SCOPE = 'user-library-read'  # TODO: For example scope i am asking to get the library of the user you can change it as you want NOUR.
SCOPE = "user-top-read,user-read-email,user-read-private"     # i figured medium-term top songs are a better way to judge rather than liked songs that can accumulate songs from years ago you no longer like (?)

token_cache = None

def login():
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE, cache_handler=token_cache, username=api.get_remote_ip())
    auth_url = sp_oauth.get_authorize_url()
    
    output = {}
    output["status"] = "ok"
    output["auth_url"] = auth_url
    return api.response(json.dumps(output))

def weblogin():
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_WEB_URI, scope=SCOPE, cache_handler=token_cache, username=api.get_remote_ip())
    auth_url = sp_oauth.get_authorize_url()
    
    return redirect(auth_url)

def callback():
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_WEB_URI, scope=SCOPE, cache_handler=token_cache, username=api.get_remote_ip())

    code = request.args.get("code")

    if not code:
        output = {}
        output["status"] = "fail"
        return api.response(json.dumps(output))

    token_info = sp_oauth.get_access_token(code)
    token = token_info["access_token"]
    
    #if not token_info:
    #    return redirect("/login")

    sp = spotipy.Spotify(auth=token)
    profile = sp.me()

    output = {}
    output["status"] = "ok"
    output["token"] = token
    output["email"] = profile["email"]

    # check if this account exists from the email
    if account.exists(profile["email"]):
        output["exists"] = True
        output["id"] = account.email_to_id(profile["email"])
    else:
        output["exists"] = False

    return api.response(json.dumps(output))

def token_from_code(code):
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE, cache_handler=token_cache, username=api.get_remote_ip())

    token_info = sp_oauth.get_access_token(code)
    token = token_info["access_token"]

    return token
