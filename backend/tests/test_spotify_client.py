import pytest
from unittest.mock import patch, MagicMock
from spotify_client import SpotifyClient


class TestSpotifyClientInitialization:
    """Test Spotify client initialization."""
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    def test_client_initialization(self):
        """Test that Spotify client can be initialized."""
        client = SpotifyClient()
        assert client.client_id == 'test_client_id'
        assert client.client_secret == 'test_client_secret'
        print("✓ Spotify client initializes correctly")
    
    @patch.dict('os.environ', {}, clear=True)
    def test_client_initialization_missing_env(self):
        """Test that client raises error when env vars are missing."""
        with pytest.raises(ValueError):
            SpotifyClient()
        print("✓ Spotify client raises error when env vars missing")


class TestAppToken:
    """Test app token functionality."""
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    def test_get_app_token_success(self, mock_post):
        """Test successful app token retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        client = SpotifyClient()
        result = client.get_app_token()
        
        assert result is True
        assert client._app_token == 'test_token'
        print("✓ App token retrieval works")
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    def test_get_app_token_failure(self, mock_post):
        """Test failed app token retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        client = SpotifyClient()
        result = client.get_app_token()
        
        assert result is False
        print("✓ App token failure handled correctly")


class TestPlaylistTracks:
    """Test playlist tracks functionality."""
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    @patch('requests.get')
    def test_get_tracks_from_playlist_success(self, mock_get, mock_post):
        """Test successful playlist tracks retrieval."""
        # Mock the token request
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_post_response
        
        # Mock the playlist request
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'items': [
                {
                    'track': {
                        'name': 'Test Song',
                        'artists': [{'name': 'Test Artist'}]
                    }
                }
            ],
            'next': None
        }
        mock_get.return_value = mock_get_response
        
        client = SpotifyClient()
        tracks = client.get_tracks_from_playlist('test_playlist_id')
        
        assert len(tracks) == 1
        assert tracks[0]['track'] == 'Test Song'
        assert tracks[0]['artist'] == 'Test Artist'
        print("✓ Playlist tracks retrieval works")
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    @patch('requests.get')
    def test_get_tracks_from_playlist_not_found(self, mock_get, mock_post):
        """Test playlist not found error."""
        # Mock the token request
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_post_response
        
        # Mock the playlist request
        mock_get_response = MagicMock()
        mock_get_response.status_code = 404
        mock_get.return_value = mock_get_response
        
        client = SpotifyClient()
        
        with pytest.raises(Exception, match="not found"):
            client.get_tracks_from_playlist('invalid_playlist_id')
        print("✓ Playlist not found error handled")


class TestSearchSong:
    """Test song search functionality."""
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    @patch('requests.get')
    def test_search_song_success(self, mock_get, mock_post):
        """Test successful song search."""
        # Mock the token request
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_post_response
        
        # Mock the search request
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'tracks': {
                'items': [
                    {
                        'id': 'test_track_id',
                        'name': 'Test Song',
                        'artists': [{'name': 'Test Artist'}],
                        'external_urls': {'spotify': 'https://spotify.com/track/test'}
                    }
                ]
            }
        }
        mock_get.return_value = mock_get_response
        
        client = SpotifyClient()
        result = client.search_song('Test Artist', 'Test Song')
        
        assert result['id'] == 'test_track_id'
        assert result['name'] == 'Test Song'
        assert result['artist'] == 'Test Artist'
        print("✓ Song search works")
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    @patch('requests.get')
    def test_search_song_no_results(self, mock_get, mock_post):
        """Test song search with no results."""
        # Mock the token request
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_post_response
        
        # Mock the search request
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'tracks': {
                'items': []
            }
        }
        mock_get.return_value = mock_get_response
        
        client = SpotifyClient()
        with pytest.raises(Exception, match="No results found"):
            client.search_song('Unknown Artist', 'Unknown Song')
        print("✓ Song search with no results handled")


class TestAddSongToPlaylist:
    """Test adding songs to playlist."""
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    def test_add_song_to_playlist_success(self, mock_post):
        """Test successful song addition to playlist."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        client = SpotifyClient(api_token='test_user_token')
        
        song_data = {
            'id': 'test_track_id',
            'name': 'Test Song',  # Use 'name' instead of 'track'
            'artist': 'Test Artist'
        }
        
        result = client.add_song_to_playlist(song_data, 'test_playlist_id')
        
        assert result is True
        print("✓ Add song to playlist works")
    
    @patch.dict('os.environ', {
        'SPOTIFY_CLIENT_ID': 'test_client_id',
        'SPOTIFY_CLIENT_SECRET': 'test_client_secret'
    })
    @patch('requests.post')
    def test_add_song_to_playlist_failure(self, mock_post):
        """Test failed song addition to playlist."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        client = SpotifyClient(api_token='test_user_token')
        
        song_data = {
            'track_id': 'test_track_id',
            'track': 'Test Song',
            'artist': 'Test Artist'
        }
        
        result = client.add_song_to_playlist(song_data, 'test_playlist_id')
        
        assert result is False
        print("✓ Add song to playlist failure handled")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])