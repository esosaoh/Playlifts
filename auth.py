from dotenv import load_dotenv
import os
import requests
import urllib.parse
import base64
from datetime import datetime
from flask import session

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://localhost:8889/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

def get_auth_url():
    scope = 'user-read-private user-read-email playlist-read-private'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return auth_url

def get_token(code):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        'Authorization': f"Basic {b64_auth_str}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    req_body = {
        'code': code,
        'grant_type': "authorization_code",
        'redirect_uri': redirect_uri,
    }
    response = requests.post(TOKEN_URL, headers=headers, data=req_body)
    return response.json()

def refresh_token():
    if 'refresh_token' not in session:
        return None
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
    return new_token_info

def get_headers():
    return {
        'Authorization': f"Bearer {session['access_token']}"
    }
