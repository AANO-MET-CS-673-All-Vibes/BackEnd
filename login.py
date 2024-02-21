from flask import Flask, redirect, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Spotify API credentials
SPOTIFY_CLIENT_ID = ''#put the client login id data
SPOTIFY_CLIENT_SECRET = ''#put the client password data . I am using the data login this way as it is redirecting to spotify url.
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'  # Update with your redirect URI so that we can login via spotify as we discussed and not with google account and then connect the spotify account with it, Though i think we should keep the login via google and then connect the music apps account in the app itself(browser version) it is kind of a standard way if we are going to give support for spotify and apple music. See what you think NOUR
SCOPE = 'user-library-read'  # For example scope i am asking to get the library of the user you can change it as you want NOUR.

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/operations')

@app.route('/operations')
def operations():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect('/login')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_saved_tracks()
    return str(results)

if __name__ == '__main__':
    app.run(debug=True)