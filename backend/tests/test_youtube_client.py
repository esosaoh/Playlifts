import pytest
from unittest.mock import patch, MagicMock
from youtube_client import YouTubeClient, Playlist, Song


class TestYouTubeClientInitialization:
    """Test YouTube client initialization."""
    
    def test_client_initialization_with_credentials(self):
        """Test that YouTube client can be initialized with credentials."""
        mock_credentials = MagicMock()
        client = YouTubeClient(credentials=mock_credentials)
        assert client.youtube_client is not None
        print("✓ YouTube client initializes with credentials")
    
    def test_client_initialization_with_api_key(self):
        """Test that YouTube client can be initialized with API key."""
        client = YouTubeClient(api_key='test_api_key')
        assert client.youtube_client is not None
        print("✓ YouTube client initializes with API key")
    
    def test_client_initialization_no_credentials(self):
        """Test that client raises error when no credentials provided."""
        with pytest.raises(ValueError):
            YouTubeClient()
        print("✓ YouTube client raises error when no credentials provided")


class TestPlaylistClass:
    """Test Playlist class."""
    
    def test_playlist_creation(self):
        """Test Playlist object creation."""
        playlist = Playlist('test_id', 'Test Playlist')
        assert playlist.id == 'test_id'
        assert playlist.title == 'Test Playlist'
        print("✓ Playlist object creation works")


class TestSongClass:
    """Test Song class."""
    
    def test_song_creation(self):
        """Test Song object creation."""
        song = Song('Test Artist', 'Test Song')
        assert song.artist == 'Test Artist'
        assert song.track == 'Test Song'
        print("✓ Song object creation works")


class TestGetVideosFromPlaylist:
    """Test getting videos from playlist."""
    
    @patch('googleapiclient.discovery.build')
    def test_get_videos_from_playlist_success(self, mock_build):
        """Test successful video retrieval from playlist."""
        mock_client = MagicMock()
        mock_playlist_items = MagicMock()
        mock_playlist_items.list.return_value.execute.return_value = {
            'items': [
                {
                    'snippet': {
                        'title': 'Test Artist - Test Song'
                    }
                }
            ]
        }
        mock_client.playlistItems.return_value = mock_playlist_items
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        songs = client.get_videos_from_playlist('test_playlist_id')
        
        assert len(songs) == 1
        assert songs[0].artist == 'Test Artist'
        assert songs[0].track == 'Test Song'
        print("✓ Get videos from playlist works")
    
    @patch('googleapiclient.discovery.build')
    def test_get_videos_from_playlist_no_artist_dash(self, mock_build):
        """Test video retrieval with title that doesn't contain artist dash."""
        mock_client = MagicMock()
        mock_playlist_items = MagicMock()
        mock_playlist_items.list.return_value.execute.return_value = {
            'items': [
                {
                    'snippet': {
                        'title': 'Just a song title without artist'
                    }
                }
            ]
        }
        mock_client.playlistItems.return_value = mock_playlist_items
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        songs = client.get_videos_from_playlist('test_playlist_id')
        
        assert len(songs) == 0
        print("✓ Get videos handles titles without artist dash")
    
    @patch('googleapiclient.discovery.build')
    def test_get_videos_from_playlist_empty(self, mock_build):
        """Test video retrieval from empty playlist."""
        mock_client = MagicMock()
        mock_playlist_items = MagicMock()
        mock_playlist_items.list.return_value.execute.return_value = {
            'items': []
        }
        mock_client.playlistItems.return_value = mock_playlist_items
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        songs = client.get_videos_from_playlist('test_playlist_id')
        
        assert len(songs) == 0
        print("✓ Get videos from empty playlist works")


class TestGetPlaylists:
    """Test getting playlists."""
    
    @patch('googleapiclient.discovery.build')
    def test_get_playlists_success(self, mock_build):
        """Test successful playlist retrieval."""
        mock_client = MagicMock()
        mock_playlists = MagicMock()
        mock_playlists.list.return_value.execute.return_value = {
            'items': [
                {
                    'id': 'playlist1',
                    'snippet': {
                        'title': 'Test Playlist 1'
                    }
                },
                {
                    'id': 'playlist2',
                    'snippet': {
                        'title': 'Test Playlist 2'
                    }
                }
            ]
        }
        mock_client.playlists.return_value = mock_playlists
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        playlists = client.get_playlists()
        
        assert len(playlists) == 2
        assert playlists[0]['id'] == 'playlist1'
        assert playlists[0]['title'] == 'Test Playlist 1'
        assert playlists[1]['id'] == 'playlist2'
        assert playlists[1]['title'] == 'Test Playlist 2'
        print("✓ Get playlists works")
    
    @patch('googleapiclient.discovery.build')
    def test_get_playlists_empty(self, mock_build):
        """Test playlist retrieval when user has no playlists."""
        mock_client = MagicMock()
        mock_playlists = MagicMock()
        mock_playlists.list.return_value.execute.return_value = {
            'items': []
        }
        mock_client.playlists.return_value = mock_playlists
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        playlists = client.get_playlists()
        
        assert len(playlists) == 0
        print("✓ Get playlists handles empty result")


class TestSearchVideos:
    """Test video search functionality."""
    
    @patch('googleapiclient.discovery.build')
    def test_search_videos_success(self, mock_build):
        """Test successful video search."""
        mock_client = MagicMock()
        mock_search = MagicMock()
        mock_search.list.return_value.execute.return_value = {
            'items': [
                {
                    'id': {
                        'videoId': 'test_video_id'
                    },
                    'snippet': {
                        'title': 'Test Video Title',
                        'description': 'Test video description',
                        'thumbnails': {
                            'default': {
                                'url': 'https://example.com/thumbnail.jpg'
                            }
                        }
                    }
                }
            ]
        }
        mock_client.search.return_value = mock_search
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        results = client.search_videos('test query', max_results=1)
        
        assert len(results) == 1
        assert results[0]['videoId'] == 'test_video_id'
        assert results[0]['title'] == 'Test Video Title'
        assert results[0]['description'] == 'Test video description'
        assert results[0]['thumbnail'] == 'https://example.com/thumbnail.jpg'
        print("✓ Search videos works")
    
    @patch('googleapiclient.discovery.build')
    def test_search_videos_no_results(self, mock_build):
        """Test video search with no results."""
        mock_client = MagicMock()
        mock_search = MagicMock()
        mock_search.list.return_value.execute.return_value = {
            'items': []
        }
        mock_client.search.return_value = mock_search
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        results = client.search_videos('nonexistent query', max_results=1)
        
        assert len(results) == 0
        print("✓ Search videos handles no results")


class TestAddVideoToPlaylist:
    """Test adding videos to playlist."""
    
    @patch('googleapiclient.discovery.build')
    def test_add_video_to_playlist_success(self, mock_build):
        """Test successful video addition to playlist."""
        mock_client = MagicMock()
        mock_playlist_items = MagicMock()
        mock_playlist_items.insert.return_value.execute.return_value = {
            'id': 'new_playlist_item_id'
        }
        mock_client.playlistItems.return_value = mock_playlist_items
        mock_build.return_value = mock_client
        
        client = YouTubeClient(api_key='test_key')
        client.add_video_to_playlist('test_playlist_id', 'test_video_id')
        
        # Verify the insert method was called with correct parameters
        mock_playlist_items.insert.assert_called_once()
        call_args = mock_playlist_items.insert.call_args
        assert call_args[1]['part'] == 'snippet'
        assert call_args[1]['body']['snippet']['playlistId'] == 'test_playlist_id'
        assert call_args[1]['body']['snippet']['resourceId']['videoId'] == 'test_video_id'
        print("✓ Add video to playlist works")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"]) 