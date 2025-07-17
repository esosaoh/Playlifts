import requests
from flask import redirect, url_for, request, session, jsonify, render_template
from flask_cors import CORS
import os
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from tasks import transfer_playlist_task
from youtube_client import YouTubeClient
from urllib.parse import urlparse, parse_qs
from spotify_client import SpotifyClient
from config import app
from celery_config import celery

load_dotenv(override=True)

IS_PROD = os.getenv("FLASK_ENV") == "production"

CORS(app, origins=[
    "https://playlifts.com", 
    "https://www.playlifts.com",
    "http://playlifts.com"
], supports_credentials=True)

app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=IS_PROD,
)

REDIRECT_URI = os.getenv('REDIRECT_URI') if IS_PROD else 'http://localhost:8889/callback'
FRONTEND_URL = 'https://playlifts.com' if IS_PROD else 'http://localhost:5173'

app.secret_key = os.getenv('SECRET_KEY')

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Playlifts API! Documentation is available at https://github.com/esosaoh/playlifts/blob/main/README.md"})

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-library-modify playlist-read-private playlist-modify-public playlist-modify-private'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True,
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return jsonify({"auth_url": auth_url})

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
            return jsonify({"status": "error", "message": f"No access token in response. Response: {token_info}"}), 400

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        session['is_logged_in'] = True

        response = redirect(FRONTEND_URL)
        response.set_cookie('is_logged_in', 'true',
                            samesite='None',
                            secure=IS_PROD,
                            httponly=False)
        return response
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-playlists', methods=['GET'])
def get_playlists():
    if 'access_token' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        }
        user_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        if user_response.status_code != 200:
            return jsonify({"error": "Failed to fetch user profile"}), 400
        user_data = user_response.json()
        current_user_id = user_data['id']

        all_playlists = []
        offset = 0
        limit = 50
        while True:
            response = requests.get(
                f'https://api.spotify.com/v1/me/playlists?limit={limit}&offset={offset}', headers=headers)
            if response.status_code != 200:
                return jsonify({"error": f"Failed to fetch playlists: {response.status_code}"}), 400
            playlists_data = response.json()
            playlists = playlists_data['items']
            if not playlists:
                break
            for playlist in playlists:
                if playlist['owner']['id'] == current_user_id:
                    cover_image = None
                    if playlist.get('images') and len(playlist['images']) > 0:
                        cover_image = playlist['images'][0]['url']
                    playlist_info = {
                        'id': playlist['id'],
                        'name': playlist['name'],
                        'tracks_count': playlist['tracks']['total'],
                        'owner': playlist['owner']['display_name'],
                        'public': playlist.get('public', False),
                        'cover_image': cover_image
                    }
                    all_playlists.append(playlist_info)
            offset += limit
            if len(playlists) < limit:
                break
        return jsonify({"playlists": all_playlists})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process-youtube', methods=['POST'])
def process_youtube():
    if 'access_token' not in session:
        return redirect(url_for('login'))

    try:
        youtube_url = request.json['url']
        target_playlist_id = request.json.get('playlist_id')

        parsed_url = urlparse(youtube_url)
        if 'youtube.com' not in parsed_url.netloc:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        query_params = parse_qs(parsed_url.query)
        playlist_id = query_params.get('list', [None])[0]

        if not playlist_id:
            return jsonify({"error": "No playlist ID found"}), 400

        task = transfer_playlist_task.delay(
            session['access_token'], playlist_id, target_playlist_id)

        return jsonify({"task_id": task.id}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/task-status/<task_id>')
def task_status(task_id):
    task = celery.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Waiting to start'}
    elif task.state == 'PROGRESS':
        progress = 0
        if hasattr(task.info, 'get'):
            progress = task.info.get('progress', 0)
        elif isinstance(task.info, dict):
            progress = task.info.get('progress', 0)
        response = {'state': task.state, 'progress': progress}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)


@app.route('/check_login', methods=['GET'])
def check_login():
    is_logged_in = session.get('is_logged_in', False)
    return jsonify({'is_logged_in': is_logged_in}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    response = jsonify({"status": "success", "message": "Logged out successfully"})
    response.delete_cookie('is_logged_in')
    return response

if __name__ == '__main__':
    app.run(port=8889, debug=not IS_PROD)
