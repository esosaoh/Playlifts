import requests
from flask import Flask, redirect, url_for, request, session, jsonify, render_template
import os
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from youtube_client import YouTubeClient
from urllib.parse import urlparse, parse_qs
from spotify_client import SpotifyClient
from config import app, db
import models

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
CREDS_PATH = os.path.join(CURRENT_DIR, 'creds', 'client_secret.json')

app.secret_key = os.getenv('SECRET_KEY')

load_dotenv(override=True)

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8889/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-library-modify'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True,
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
         return jsonify({"status": "error", "message": request.args['error']}), 400
    
    if 'code' not in request.args:
        return jsonify({"status": "error", "message": "Authorization code not found"}), 400
    
    try:
        auth_code = request.args['code']

        req_body = {
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }

        
        response = requests.post(TOKEN_URL, data=req_body)

        if response.status_code != 200:
            return jsonify({"status": "error", "message": f"Token request failed with status {response.status_code}"}), 400

        token_info = response.json()
        
        if 'access_token' not in token_info:
            error_msg = f"No access token in response. Response: {token_info}"
            return jsonify({"status": "error", "message": error_msg}), 400

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        session['is_logged_in'] = True

        return jsonify({"status": "success", "message": "Authorization successful"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/process-youtube', methods=['POST'])
def process_youtube():
    if 'access_token' not in session:
        return redirect(url_for('login'))

    try:
        youtube_url = request.json['url']
        # Extract playlist ID from URL
        parsed_url = urlparse(youtube_url)
        if 'youtube.com' not in parsed_url.netloc:
            return jsonify({"error": "Not a valid YouTube URL"}), 400
            
        query_params = parse_qs(parsed_url.query)
        playlist_id = query_params.get('list', [None])[0]
        
        if not playlist_id:
            return jsonify({"error": "Could not find playlist ID in URL"}), 400

        youtube_client = YouTubeClient(YOUTUBE_API_KEY)
        spotify_client = SpotifyClient(session['access_token'])
        
        songs = youtube_client.get_videos_from_playlist(playlist_id)
        successful_transfers = []
        failed_transfers = []

        for song in songs:
            try:
                spotify_song_id = spotify_client.search_song(song.artist, song.track)
                if spotify_client.add_song_to_spotify(spotify_song_id):
                    successful_transfers.append({
                        'artist': song.artist,
                        'track': song.track
                    })
                else:
                    failed_transfers.append({
                        'artist': song.artist,
                        'track': song.track,
                        'reason': 'Failed to add to Spotify'
                    })
            except Exception as e:
                failed_transfers.append({
                    'artist': song.artist,
                    'track': song.track,
                    'reason': str(e)
                })

        return jsonify({
            'success': {
                'count': len(successful_transfers),
                'songs': successful_transfers
            },
            'failed': {
                'count': len(failed_transfers),
                'songs': failed_transfers
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def get_user_id():
    if 'access_token' not in session:
        return None 
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    user_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    if user_response.status_code != 200:
        return None 
    user_data = user_response.json()

    return user_data.get('id')
    
if __name__ == '__main__':
    #with app.app_context():
     #   db.create_all()
    app.run(port=8889, debug=True)
    