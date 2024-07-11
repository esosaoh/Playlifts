from flask import Flask, redirect, request, jsonify, session
from datetime import datetime
import requests
import auth

app = Flask(__name__)
app.secret_key = '5bvrhjg4-g48n3ug-nrjg5g-G03g'

@app.route('/')
def index():
    return "Welcome to ListenUP <a href='/login'>Log in with Spotify</a>"

@app.route('/login')
def login():
    return redirect(auth.get_auth_url())

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    if 'code' in request.args:
        token_info = auth.get_token(request.args['code'])
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
    headers = auth.get_headers()
    response = requests.get(auth.API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    new_token_info = auth.refresh_token()
    if not new_token_info:
        return redirect('/login')
    return redirect('/playlists')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)










