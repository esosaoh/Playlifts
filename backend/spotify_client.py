import os
import base64
import requests
import time
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

logger = logging.getLogger(__name__)

class SpotifyClient:
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize Spotify client.
        
        Args:
            api_token: User access token (for user-specific operations)
                      If None, will use Client Credentials for public data
        """
        self.api_token = api_token
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.base_url = 'https://api.spotify.com/v1'
        self._app_token = None
        self._app_token_expires_at = 0
        
        if not self.client_id or not self.client_secret:
            raise ValueError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set")
    
    def get_app_token(self) -> bool:
        """
        Get or refresh the Client Credentials (app-only) token.
        This token can access public playlists without user authentication.
        """
        current_time = time.time()
        
        if self._app_token and current_time < self._app_token_expires_at:
            return True
        
        try:
            auth_str = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_str.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'client_credentials'
            }
            
            response = requests.post(
                'https://accounts.spotify.com/api/token',
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self._app_token = token_data['access_token']
                expires_in = token_data.get('expires_in', 3600)
                self._app_token_expires_at = current_time + expires_in - 60  # 1 minute buffer
                logger.info("Successfully obtained Spotify app token")
                return True
            else:
                logger.error(f"Failed to get app token: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error getting app token: {str(e)}")
            return False
    
    def _get_headers(self, use_app_token: bool = False) -> Dict[str, str]:
        """Get headers for API requests."""
        if use_app_token:
            if not self.get_app_token():
                raise Exception("Failed to get app token")
            token = self._app_token
        else:
            if not self.api_token:
                raise Exception("No user token available")
            token = self.api_token
        
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def get_tracks_from_playlist(self, playlist_id: str) -> List[Dict[str, Any]]:
        """
        Get up to 15 tracks from a PUBLIC Spotify playlist using Client Credentials.
        Returns a list of dicts with only 'track' and 'artist' keys for frontend compatibility.
        """
        try:
            headers = self._get_headers(use_app_token=True)
            tracks = []
            offset = 0
            limit = 50
            max_tracks = 15
            
            while len(tracks) < max_tracks:
                url = f"{self.base_url}/playlists/{playlist_id}/tracks"
                params = {
                    'offset': offset,
                    'limit': limit,
                    'fields': 'items(track(name,artists(name))),next'
                }
                
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    
                    for item in items:
                        if len(tracks) >= max_tracks:
                            break
                        track = item.get('track')
                        if track and track.get('name'):
                            artists = [artist['name'] for artist in track.get('artists', [])]
                            tracks.append({
                                'track': track['name'],
                                'artist': ', '.join(artists)
                            })
                    
                    if not data.get('next') or len(tracks) >= max_tracks:
                        break
                    
                    offset += limit
                    
                elif response.status_code == 404:
                    raise Exception(f"Playlist {playlist_id} not found or is private")
                elif response.status_code == 401:
                    raise Exception("Authentication failed - playlist may be private")
                else:
                    raise Exception(f"API error: {response.status_code} - {response.text}")
            
            logger.info(f"Retrieved {len(tracks)} tracks (max 15) from playlist {playlist_id}")
            return tracks
            
        except Exception as e:
            logger.error(f"Error getting tracks from playlist {playlist_id}: {str(e)}")
            raise
    
    def search_song(self, artist: str, track: str) -> Dict[str, Any]:
        """
        Search for a song on Spotify.
        Uses user token if available, otherwise uses app token.
        """
        try:
            use_app_token = self.api_token is None
            headers = self._get_headers(use_app_token=use_app_token)
                
            query = f'artist:"{artist}" track:"{track}"'
            
            params = {
                'q': query,
                'type': 'track',
                'limit': 1
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                tracks = data.get('tracks', {}).get('items', [])
                
                if tracks:
                    track_data = tracks[0]
                    artists = [artist['name'] for artist in track_data.get('artists', [])]
                    
                    return {
                        'id': track_data['id'],
                        'name': track_data['name'],
                        'artist': ', '.join(artists),
                        'artists': artists,
                        'external_urls': track_data.get('external_urls', {}),
                        'artwork_url': track_data.get('album', {}).get('images', [{}])[0].get('url')
                    }
                else:
                    raise Exception(f"No results found for '{artist} - {track}'")
            else:
                raise Exception(f"Search API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error searching for song '{artist} - {track}': {str(e)}")
            raise
    
    def add_song_to_playlist(self, song_data: Dict[str, Any], playlist_id: str) -> bool:
        """
        Add a song to a Spotify playlist.
        Requires user token with playlist modification permissions.
        """
        if not self.api_token:
            raise Exception("User token required for playlist modification")
        
        try:
            headers = self._get_headers(use_app_token=False)
            
            data = {
                'uris': [f"spotify:track:{song_data['id']}"]
            }
            
            response = requests.post(
                f"{self.base_url}/playlists/{playlist_id}/tracks",
                headers=headers,
                json=data
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"Successfully added '{song_data['name']}' to playlist {playlist_id}")
                return True
            else:
                logger.error(f"Failed to add song to playlist: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding song to playlist: {str(e)}")
            return False
    
    def add_song_to_spotify(self, song_data: Dict[str, Any]) -> bool:
        """
        Add a song to user's Liked Songs.
        Requires user token with user-library-modify scope.
        """
        if not self.api_token:
            raise Exception("User token required for adding to liked songs")
        
        try:
            headers = self._get_headers(use_app_token=False)
            
            data = {
                'ids': [song_data['id']]
            }
            
            response = requests.put(
                f"{self.base_url}/me/tracks",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully added '{song_data['name']}' to liked songs")
                return True
            else:
                logger.error(f"Failed to add song to liked songs: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding song to liked songs: {str(e)}")
            return False