from flask import session
from app import app
from spotify_client import SpotifyClient

#spotify client test
with app.test_client() as client:
    with client.session_transaction() as session:
        access_token = session.get('access_token')
        if access_token:
            spotify = SpotifyClient(access_token)
            print(spotify.search_song("Coldplay", "Viva la Vida"))
        else:
            print("No access token found. Please login through the web app first.")