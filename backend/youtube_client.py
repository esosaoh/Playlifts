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


class YouTubeClient(object):
    def __init__(self, api_key):
        youtube_dl.utils.std_headers['User-Agent'] = "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
        
        self.youtube_client = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key)

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