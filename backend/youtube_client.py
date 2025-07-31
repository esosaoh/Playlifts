import googleapiclient.discovery
import youtube_dl


class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track
    
    def __str__(self):
        return f"{self.artist} - {self.track}"


class YouTubeClient(object):
    def __init__(self, credentials=None, api_key=None):
        youtube_dl.utils.std_headers['User-Agent'] = "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"

        self.youtube_client = None
        if credentials:
            self.youtube_client = googleapiclient.discovery.build(
                "youtube", "v3", credentials=credentials)
        elif api_key:
            self.youtube_client = googleapiclient.discovery.build(
                "youtube", "v3", developerKey=api_key)
        else:
            raise ValueError("YouTubeClient requires credentials or api_key")

    def get_videos_from_playlist(self, playlist_id):
        songs = []
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="snippet",
            maxResults=50
        )
        response = request.execute()

        for item in response['items']:
            try:
                title = item['snippet']['title']
                
                if ' - ' in title:
                    artist, track = title.split(' - ', 1)
                    track = track.split('(')[0].split('[')[0].strip()
                    artist = artist.strip()
                    if artist and track:
                        songs.append(Song(artist, track))
            except:
                continue
        return songs

    def get_playlists(self):
        playlists = []
        request = self.youtube_client.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50
        )
        response = request.execute()
        for item in response.get('items', []):
            playlists.append({
                'id': item['id'],
                'title': item['snippet']['title']
            })
        return playlists

    def search_videos(self, query, max_results=25):
        results = []
        request = self.youtube_client.search().list(
            q=query,
            part="snippet",
            maxResults=max_results,
            type="video"
        )
        response = request.execute()
        for item in response.get('items', []):
            results.append({
                'videoId': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            })
        return results

    def add_video_to_playlist(self, playlist_id, video_id):
        request_body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }

        request = self.youtube_client.playlistItems().insert(
            part="snippet",
            body=request_body
        )
        response = request.execute()
        return response
