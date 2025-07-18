import requests
from flask import redirect, url_for, request, session, jsonify
from flask_cors import CORS
import os
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from tasks import transfer_playlist_task, transfer_spotify_to_youtube_task
from youtube_client import YouTubeClient
from urllib.parse import urlparse, parse_qs
from spotify_client import SpotifyClient
from config import app
from celery_config import celery
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest

load_dotenv(override=True)

CORS(app, origins=[
    "https://playlifts.com",
    "https://www.playlifts.com"
], supports_credentials=True)

app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,
)

SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
FRONTEND_URL = 'https://playlifts.com'

app.secret_key = os.getenv('SECRET_KEY')

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_youtube_credentials():
    if 'youtube_token' not in session:
        return None

    creds_data = session['youtube_token']
    credentials = Credentials(
        token=creds_data['token'],
        refresh_token=creds_data.get('refresh_token'),
        token_uri=creds_data['token_uri'],
        client_id=creds_data['client_id'],
        client_secret=creds_data['client_secret'],
        scopes=creds_data['scopes']
    )
    # refresh token expiring
    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(GoogleRequest())
                session['youtube_token'] = {
                    "token": credentials.token,
                    "refresh_token": credentials.refresh_token,
                    "token_uri": credentials.token_uri,
                    "client_id": credentials.client_id,
                    "client_secret": credentials.client_secret,
                    "scopes": credentials.scopes
                }
            except Exception as e:
                app.logger.error(f"Failed to refresh YouTube token: {e}")
                return None
        else:
            return None
    return credentials

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Playlifts API! Documentation is available at https://github.com/esosaoh/playlifts/blob/main/README.md"})

@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/spotify/login')
def spotify_login():
    scope = 'user-read-private user-read-email user-library-modify playlist-read-private playlist-modify-public playlist-modify-private'

    params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'show_dialog': True,
    }

    auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return jsonify({"auth_url": auth_url})

@app.route('/spotify/callback')
def spotify_callback():
    if 'error' in request.args:
        return jsonify({"status": "error", "message": request.args['error']}), 400
    if 'code' not in request.args:
        return jsonify({"status": "error", "message": "Authorization code not found"}), 400
    try:
        auth_code = request.args['code']

        req_body = {
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        }

        response = requests.post(SPOTIFY_TOKEN_URL, data=req_body)

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
                            secure=True,
                            httponly=False)
        return response
    except Exception:
        app.logger.exception("Error in callback")
        raise

@app.route('/spotify/playlists', methods=['GET'])
def spotify_playlists():
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
    except Exception:
        app.logger.exception("Error in get_playlists")
        raise


@app.route('/spotify/transfer', methods=['POST'])
def spotify_transfer():
    if 'access_token' not in session:
        return jsonify({"error": "Not authenticated with Spotify"}), 401

    credentials = get_youtube_credentials()
    if not credentials:
        return jsonify({"error": "Not authenticated with YouTube"}), 401

    data = request.json
    spotify_playlist_id = data.get('spotify_playlist_id')
    youtube_playlist_id = data.get('youtube_playlist_id')

    if not spotify_playlist_id or not youtube_playlist_id:
        return jsonify({"error": "Missing playlist IDs"}), 400

    youtube_token_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }

    task = transfer_spotify_to_youtube_task.delay(
        session['access_token'],
        spotify_playlist_id,
        youtube_playlist_id,
        youtube_token_data
    )
    return jsonify({"task_id": task.id}), 202

@app.route('/youtube/login')
def youtube_login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=YOUTUBE_SCOPES
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    session['google_oauth_state'] = state
    return jsonify({"auth_url": auth_url})

@app.route('/youtube/callback')
def youtube_callback():
    state = session.get('google_oauth_state')
    if not state:
        return jsonify({"error": "Invalid OAuth state"}), 400
    if request.args.get('state') != state:
        return jsonify({"error": "State mismatch"}), 400

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=YOUTUBE_SCOPES,
        state=state
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['youtube_token'] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }
    session['is_youtube_logged_in'] = True

    response = redirect(FRONTEND_URL)
    response.set_cookie('is_youtube_logged_in', 'true',
                        samesite='None', secure=True, httponly=False)
    return response

@app.route('/youtube/playlists')
def youtube_playlists():
    credentials = get_youtube_credentials()
    if not credentials:
        return jsonify({"error": "Not authenticated with YouTube or token refresh failed"}), 401

    yt_client = YouTubeClient(credentials=credentials)
    playlists = yt_client.get_playlists()
    return jsonify({"playlists": playlists})

@app.route('/youtube/transfer', methods=['POST'])
def youtube_transfer():
    if 'access_token' not in session:
        return redirect(url_for('spotify_login'))

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
    except Exception:
        app.logger.exception("Error in process_youtube")
        raise

@app.route('/auth/check', methods=['GET'])
def check_login():
    is_logged_in = session.get('is_logged_in', False)
    return jsonify({'is_logged_in': is_logged_in}), 200

@app.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    response = jsonify({"status": "success", "message": "Logged out successfully"})
    response.delete_cookie('is_logged_in')
    return response

@app.route('/tasks/status/<task_id>')
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


if __name__ == '__main__':
    app.run(port=8889, debug=False)
