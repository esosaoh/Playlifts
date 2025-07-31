import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_spotify_session():
    """Mock Spotify session data."""
    return {
        'access_token': 'mock_spotify_token',
        'refresh_token': 'mock_refresh_token',
        'expires_at': 1234567890.0,
        'is_logged_in': True
    }


@pytest.fixture
def mock_youtube_session():
    """Mock YouTube session data."""
    return {
        'youtube_token': {
            'token': 'mock_youtube_token',
            'refresh_token': 'mock_refresh_token',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': 'mock_client_id',
            'client_secret': 'mock_client_secret',
            'scopes': ['https://www.googleapis.com/auth/youtube.force-ssl']
        }
    }


@pytest.fixture
def sample_playlist_data():
    """Sample playlist data for testing."""
    return {
        'id': 'test_playlist_id',
        'title': 'Test Playlist',
        'tracks': [
            {'track': 'Test Song 1', 'artist': 'Test Artist 1'},
            {'track': 'Test Song 2', 'artist': 'Test Artist 2'}
        ]
    }


@pytest.fixture
def sample_song_data():
    """Sample song data for testing."""
    return {
        'track': 'Test Song',
        'artist': 'Test Artist',
        'artwork_url': 'https://example.com/artwork.jpg'
    } 