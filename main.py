from dotenv import load_dotenv
import os
from flask import Flask, redirect, request, jsonify, session
import requests
import urllib.parse
from datetime import datetime
import base64

load_dotenv()

app = Flask(__name__)
app.secret_key = '5bvrhjg4-g48n3ug-nrjg5g-G03g'  


client_id=os.getenv('CLIENT_ID')
client_secret=os.getenv('CLIENT_SECRET')
redirect_uri = 'http://localhost:8889/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize' 
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return "Welcome to ListenUP <a href='/login'>Log in with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-read-private'

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True  # for debugging purposes, change to false for production
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        # Encode client ID and client secret
        auth_str = f"{client_id}:{client_secret}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {
            'Authorization': f"Basic {b64_auth_str}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req_body = {
            'code': request.args['code'],
            'grant_type': "authorization_code",
            'redirect_uri': redirect_uri,
        }

        response = requests.post(TOKEN_URL, headers=headers, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlists')

@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }


    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': session['refresh_token'],
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return redirect('/playlists')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)










