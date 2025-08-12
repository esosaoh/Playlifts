import os
import time
import logging

from dotenv import load_dotenv
from celery import current_task
from config.celery_config import celery
from celery.exceptions import Ignore

from clients.youtube_client import YouTubeClient
from clients.spotify_client import SpotifyClient
from google.oauth2.credentials import Credentials

load_dotenv(override=True)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery.task(bind=True)
def transfer_playlist_task(self, access_token, playlist_id, target_playlist_id):
    """
    YouTube -> Spotify transfer.
    access_token: Spotify *user* token (must have modify scopes).
    playlist_id: YouTube playlist ID (source).
    target_playlist_id: Spotify playlist ID (dest) OR None -> save to Liked Songs.
    """
    try:
        youtube_client = YouTubeClient(api_key=YOUTUBE_API_KEY)
        spotify_client = SpotifyClient(api_token=access_token)

        songs = youtube_client.get_videos_from_playlist(playlist_id)
        total_songs = len(songs)

        successful_transfers = []
        failed_transfers = []

        self.update_state(
            state="PROGRESS",
            meta={
                "current": 0,
                "total": total_songs,
                "progress": 0,
                "status": f"Starting transfer of {total_songs} songs...",
            },
        )

        for i, song in enumerate(songs):
            try:
                if i > 0 and i % 10 == 0:
                    time.sleep(1)  # basic rate pacing

                spotify_song_data = spotify_client.search_song(song.artist, song.track)
                if target_playlist_id:
                    success = spotify_client.add_song_to_playlist(
                        spotify_song_data, target_playlist_id
                    )
                else:
                    success = spotify_client.add_song_to_spotify(spotify_song_data)

                if success:
                    successful_transfers.append(
                        {
                            "artist": spotify_song_data["artist"],
                            "track": spotify_song_data["name"],
                            "artwork_url": spotify_song_data.get("artwork_url"),
                        }
                    )
                else:
                    failed_transfers.append(
                        {
                            "artist": song.artist,
                            "track": song.track,
                            "reason": "Failed to add to Spotify",
                        }
                    )
            except Exception as e:
                failed_transfers.append(
                    {"artist": song.artist, "track": song.track, "reason": str(e)}
                )

            if i % 2 == 0 or i == total_songs - 1:
                progress = (i + 1) / total_songs * 100 if total_songs else 100
                self.update_state(
                    state="PROGRESS",
                    meta={
                        "current": i + 1,
                        "total": total_songs,
                        "progress": progress,
                        "status": f"Processed {i + 1}/{total_songs} songs",
                    },
                )

        return {
            "success": {
                "count": len(successful_transfers),
                "songs": successful_transfers,
            },
            "failed": {"count": len(failed_transfers), "songs": failed_transfers},
        }

    except Exception as e:
        logger.error(f"Task failed with error: {str(e)}", exc_info=True)
        raise


@celery.task(bind=True)
def transfer_spotify_to_youtube_task(
    self,
    _unused_access_token,
    spotify_playlist_id,
    youtube_playlist_id,
    youtube_token_data,
):
    """
    Spotify -> YouTube transfer.
    spotify_playlist_id: Source Spotify playlist (public).
    youtube_playlist_id: Destination YouTube playlist (must belong to authorized user).
    youtube_token_data: dict containing YouTube OAuth credentials (token, refresh_token, etc.).
    """
    try:
        logger.info(
            f"Starting Spotify to YouTube transfer: {spotify_playlist_id} -> {youtube_playlist_id}"
        )

        spotify_client = SpotifyClient(api_token=None)

        if not spotify_client.get_app_token():
            raise Exception("Failed to get Spotify app token")

        credentials = Credentials(
            token=youtube_token_data["token"],
            refresh_token=youtube_token_data.get("refresh_token"),
            token_uri=youtube_token_data["token_uri"],
            client_id=youtube_token_data["client_id"],
            client_secret=youtube_token_data["client_secret"],
            scopes=youtube_token_data["scopes"],
        )
        youtube_client = YouTubeClient(credentials=credentials)

        self.update_state(
            state="PROGRESS",
            meta={
                "current": 0,
                "total": 0,
                "progress": 0,
                "status": "Fetching Spotify playlist...",
            },
        )

        tracks = spotify_client.get_tracks_from_playlist(spotify_playlist_id)
        total_tracks = len(tracks)

        logger.info(f"Found {total_tracks} tracks in Spotify playlist")

        successful = []
        failed = []

        self.update_state(
            state="PROGRESS",
            meta={
                "current": 0,
                "total": total_tracks,
                "progress": 0,
                "status": "Starting transfer...",
            },
        )

        for i, track in enumerate(tracks):
            try:
                query = f"{track['artist']} - {track['track']}"
                logger.info(f"Searching YouTube for: {query}")

                search_results = youtube_client.search_videos(query, max_results=1)
                if search_results:
                    video_id = search_results[0]["videoId"]
                    youtube_client.add_video_to_playlist(youtube_playlist_id, video_id)
                    successful.append(track)
                    logger.info(f"Successfully added: {query}")
                else:
                    failed.append({"track": track, "reason": "No YouTube video found"})
                    logger.warning(f"No YouTube video found for: {query}")

                if i % 5 == 0:
                    time.sleep(1)

            except Exception as e:
                error_msg = str(e)
                failed.append({"track": track, "reason": error_msg})
                logger.error(
                    f"Error processing track {track.get('track', 'Unknown')} by {track.get('artist', 'Unknown')}: {error_msg}"
                )

            if i % 2 == 0 or i == total_tracks - 1:
                progress = (i + 1) / total_tracks * 100 if total_tracks else 100
                self.update_state(
                    state="PROGRESS",
                    meta={
                        "current": i + 1,
                        "total": total_tracks,
                        "progress": progress,
                        "status": f"Processed {i + 1}/{total_tracks} tracks",
                    },
                )

        result = {
            "success": {"count": len(successful), "tracks": successful},
            "failed": {"count": len(failed), "tracks": failed},
        }

        logger.info(
            f"Transfer completed: {len(successful)} successful, {len(failed)} failed"
        )
        return result

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Task failed with error: {error_msg}", exc_info=True)
        raise
