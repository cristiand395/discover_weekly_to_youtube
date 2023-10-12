import spotipy
import time 
from spotipy.oauth2 import SpotifyOAuth
import os
from flask import Flask, request, redirect, session, url_for

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Access environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
# YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
app.secret_key = '9usd0f9sdfs0d9f'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info

    return redirect(url_for('save_discover_weekly', external = True))


@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')
    
    sp = spotipy.Spotify(auth = token_info['access_token'])
    user_id = sp.current_user()['id']
    saved_weekly_playlist_id = None

    current_playlists = sp.current_user_playlists()['items']
    for playlist in current_playlists:
        if playlist['name'] == 'Discover Weekly':
            print("Discover Weekly playlist found")
            discover_weekly_playlist_id = playlist['id']
        if playlist['name'] == 'Saved Weekly':
            print("Saved Weekly playlist found")
            saved_weekly_playlist_id = playlist['id']

    if not discover_weekly_playlist_id:
        return "Discover Weekly playlist not found"
    
    if not saved_weekly_playlist_id:
        new_playlist = sp.user_playlist_create(user_id, 'Saved Weekly', public=False)
        saved_weekly_playlist_id = new_playlist['id']

    discover_weekly_playlist = sp.playlist_items(discover_weekly_playlist_id)
    song_urls = []
    for song in discover_weekly_playlist['items']:
        song_uri = song['track']['uri']
        song_urls.append(song_uri)

    sp.user_playlist_add_tracks(user_id, saved_weekly_playlist_id, song_urls)
    return "Playlist saved"


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return redirect(url_for('login', external = False))
    
    now = int(time.time())  
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = SPOTIFY_CLIENT_ID,
        client_secret = SPOTIFY_CLIENT_SECRET,
        redirect_uri = url_for(endpoint='redirect_page', _external = True) ,
        scope = 'user-library-read playlist-modify-public playlist-modify-private'
    )

app.run(debug=True, port=8080)

