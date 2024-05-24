import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

username = os.getenv("SPOTIFY_USER")
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
auth_manager = SpotifyOAuth(
    scope="user-read-currently-playing",
    username=username,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
)

spotipy.Spotify(auth_manager=auth_manager).currently_playing()
