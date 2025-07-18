import requests
import urllib.parse


class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token
    
    def search_song(self, artist, track):
        query = urllib.parse.quote(f'{artist} {track}')
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        response_json = response.json()
        
        results = response_json['tracks']['items']
        
        if results:
            # assume the first track in the list is the song we want
            track_data = results[0]
            artwork_url = None
            if track_data.get('album') and track_data['album'].get('images'):
                artwork_url = track_data['album']['images'][0]['url']
            
            return {
                'id': track_data['id'],
                'name': track_data['name'],
                'artist': track_data['artists'][0]['name'] if track_data['artists'] else artist,
                'artwork_url': artwork_url
            }
        else:
            raise Exception(f"No song found for {artist} = {track}")
    
    def add_song_to_spotify(self, song_data):
        song_id = song_data['id'] if isinstance(song_data, dict) else song_data
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        
        return response.ok
    
    def add_song_to_playlist(self, song_data, playlist_id):
        song_id = song_data['id'] if isinstance(song_data, dict) else song_data
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.post(
            url,
            json={
                "uris": [f"spotify:track:{song_id}"]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        
        return response.ok

    def get_tracks_from_playlist(self, playlist_id):
        tracks = []
        limit = 100
        offset = 0

        while True:
            url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}&offset={offset}"
            response = requests.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_token}"
                }
            )
            if response.status_code != 200:
                raise Exception(f"Failed to get playlist tracks: {response.status_code} - {response.text}")

            data = response.json()
            items = data.get('items', [])

            if not items:
                break

            for item in items:
                track = item.get('track')
                if not track:
                    continue
                track_name = track.get('name')
                artists = track.get('artists', [])
                artist_name = artists[0]['name'] if artists else None

                if track_name and artist_name:
                    tracks.append({
                        'name': track_name,
                        'artist': artist_name
                    })

            if data.get('next'):
                offset += limit
            else:
                break

        return tracks
