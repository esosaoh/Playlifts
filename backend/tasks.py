from celery import current_task
from youtube_client import YouTubeClient
from spotify_client import SpotifyClient
import os
from dotenv import load_dotenv
import time
from celery_config import celery

load_dotenv(override=True)

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

@celery.task(bind=True)
def transfer_playlist_task(self, access_token, playlist_id, target_playlist_id):
    """Celery task to handle large playlist transfers"""
    try:
        youtube_client = YouTubeClient(YOUTUBE_API_KEY)
        spotify_client = SpotifyClient(access_token)
        
        songs = youtube_client.get_videos_from_playlist(playlist_id)
        total_songs = len(songs)
        
        successful_transfers = []
        failed_transfers = []
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': total_songs,
                'progress': 0,
                'status': f'Starting transfer of {total_songs} songs...'
            }
        )
        
        for i, song in enumerate(songs):
            try:
                if i > 0 and i % 10 == 0:
                    time.sleep(1)
                
                spotify_song_data = spotify_client.search_song(song.artist, song.track)
                if target_playlist_id:
                    success = spotify_client.add_song_to_playlist(spotify_song_data, target_playlist_id)
                else:
                    success = spotify_client.add_song_to_spotify(spotify_song_data)
                
                if success:
                    successful_transfers.append({
                        'artist': spotify_song_data['artist'],
                        'track': spotify_song_data['name'],
                        'artwork_url': spotify_song_data.get('artwork_url')
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
            
            # Update progress every 2 songs for more responsive UI
            if i % 2 == 0 or i == total_songs - 1:
                progress = (i + 1) / total_songs * 100
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'current': i + 1,
                        'total': total_songs,
                        'progress': progress,
                        'status': f'Processed {i + 1}/{total_songs} songs'
                    }
                )

        return {
            'success': {
                'count': len(successful_transfers),
                'songs': successful_transfers
            },
            'failed': {
                'count': len(failed_transfers),
                'songs': failed_transfers
            }
        }
        
    except Exception as e:
        self.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise
