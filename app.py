from flask import Flask, redirect, request, jsonify, session
from datetime import datetime
import requests
import auth

app = Flask(__name__)
app.secret_key = '5bvrhjg4-g48n3ug-nrjg5g-G03g'

@app.route('/')
def index():
    return """
    Welcome to ListenUP<br>
    <a href='/login'>Log in with Spotify</a><br>
    <a href='/top/artists'>View Top Artists</a><br>
    <a href='/top/tracks'>View Top Tracks</a>
    """

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

@app.route('/top/<type>')
def get_top_artists(type):
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    params = {
        'time_range': 'short_term'
    }
    if 'time_range' in request.args:
        time_range = requests.args.get('time_range')
        params['time_range'] = time_range

    if 'limit' in request.args:
        limit = request.args.get('limit')
        params['limit'] = limit

    if 'offset' in request.args:
        offset = request.args.get('offset') 

    headers = auth.get_headers()
    response = requests.get(
        f"{auth.API_BASE_URL}me/top/{type}",
        headers=headers,
        params=params
    )

    data = response.json()

     # Get the actual values used
    actual_offset = params.get('offset', 0)
    
    # Process the response based on type
    if type == 'tracks':
        processed_items = [{
            'rank': i + actual_offset + 1,
            'name': item['name'],
            'artist': item['artists'][0]['name'],
            'album': item['album']['name'],
            'popularity': item['popularity'],
            'preview_url': item['preview_url'],
            'spotify_url': item['external_urls']['spotify']
        } for i, item in enumerate(data['items'])]
    else:  # artists
        processed_items = [{
            'rank': i + actual_offset + 1,
            'name': item['name'],
            'genres': item['genres'],
            'popularity': item['popularity'],
            'followers': item['followers']['total'],
            'spotify_url': item['external_urls']['spotify']
        } for i, item in enumerate(data['items'])]
    
    return jsonify({
        'total': data['total'],
        'offset': actual_offset,
        'limit': len(processed_items),
        'time_range': params['time_range'],  # Include time_range in response
        'items': processed_items
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)










