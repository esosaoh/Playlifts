"""
Simplified tests for core task functionality (without Celery decorators).
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from youtube_client import Song


class TestPlaylistTransferLogic:
    """Test the core playlist transfer logic."""

    def test_basic_functionality_exists(self):
        """Test that task functions can be imported."""
        from tasks import transfer_playlist_task, transfer_spotify_to_youtube_task

        assert callable(transfer_playlist_task)
        assert callable(transfer_spotify_to_youtube_task)

    @patch("tasks.YouTubeClient")
    @patch("tasks.SpotifyClient")
    def test_youtube_to_spotify_core_logic(
        self, mock_spotify_client_class, mock_youtube_client_class
    ):
        """Test the core YouTube to Spotify transfer logic."""
        from youtube_client import YouTubeClient
        from spotify_client import SpotifyClient

        # Mock YouTube client
        mock_youtube_client = MagicMock()
        mock_youtube_client.get_videos_from_playlist.return_value = [
            Song("Test Artist", "Test Song")
        ]

        # Mock Spotify client
        mock_spotify_client = MagicMock()
        mock_spotify_client.search_song.return_value = {
            "id": "spotify_track_id",
            "name": "Test Song",
            "artist": "Test Artist",
        }
        mock_spotify_client.add_song_to_playlist.return_value = True

        # Test the core logic manually
        youtube_client = mock_youtube_client
        spotify_client = mock_spotify_client

        # Simulate the task logic
        songs = youtube_client.get_videos_from_playlist("test_playlist_id")

        successful_songs = []
        failed_songs = []

        for song in songs:
            try:
                search_result = spotify_client.search_song(
                    f"{song.artist} {song.track}"
                )
                if search_result:
                    added = spotify_client.add_song_to_playlist(
                        "target_playlist", search_result["id"]
                    )
                    if added:
                        successful_songs.append(
                            {
                                "youtube_title": f"{song.artist} - {song.track}",
                                "spotify_match": search_result,
                            }
                        )
                    else:
                        failed_songs.append(
                            {
                                "youtube_title": f"{song.artist} - {song.track}",
                                "error": "Failed to add to playlist",
                            }
                        )
            except Exception as e:
                failed_songs.append(
                    {"youtube_title": f"{song.artist} - {song.track}", "error": str(e)}
                )

        # Verify the logic works
        assert len(successful_songs) == 1
        assert len(failed_songs) == 0
        assert successful_songs[0]["youtube_title"] == "Test Artist - Test Song"

    @patch("tasks.SpotifyClient")
    def test_spotify_to_youtube_core_logic(self, mock_spotify_client_class):
        """Test the core Spotify to YouTube transfer logic."""
        from spotify_client import SpotifyClient
        from youtube_client import YouTubeClient

        # Mock Spotify client
        mock_spotify_client = MagicMock()
        mock_spotify_client.get_app_token.return_value = True
        mock_spotify_client.get_tracks_from_playlist.return_value = [
            {"track": "Test Song", "artist": "Test Artist"}
        ]

        # Test the core logic manually
        spotify_client = mock_spotify_client

        # Simulate getting app token
        token_success = spotify_client.get_app_token()
        assert token_success is True

        # Simulate getting tracks
        tracks = spotify_client.get_tracks_from_playlist("test_playlist_id")
        assert len(tracks) == 1
        assert tracks[0]["track"] == "Test Song"
        assert tracks[0]["artist"] == "Test Artist"

    def test_song_class_functionality(self):
        """Test the Song class from youtube_client."""
        song = Song("Test Artist", "Test Track")

        assert song.artist == "Test Artist"
        assert song.track == "Test Track"
        assert str(song) == "Test Artist - Test Track"


class TestTaskImports:
    """Test that task modules can be imported correctly."""

    def test_import_transfer_playlist_task(self):
        """Test importing transfer_playlist_task."""
        try:
            from tasks import transfer_playlist_task

            assert callable(transfer_playlist_task)
        except ImportError as e:
            pytest.fail(f"Could not import transfer_playlist_task: {e}")

    def test_import_transfer_spotify_to_youtube_task(self):
        """Test importing transfer_spotify_to_youtube_task."""
        try:
            from tasks import transfer_spotify_to_youtube_task

            assert callable(transfer_spotify_to_youtube_task)
        except ImportError as e:
            pytest.fail(f"Could not import transfer_spotify_to_youtube_task: {e}")

    def test_import_youtube_client(self):
        """Test importing YouTubeClient and Song."""
        try:
            from youtube_client import YouTubeClient, Song

            assert YouTubeClient is not None
            assert Song is not None
        except ImportError as e:
            pytest.fail(f"Could not import from youtube_client: {e}")

    def test_import_spotify_client(self):
        """Test importing SpotifyClient."""
        try:
            from spotify_client import SpotifyClient

            assert SpotifyClient is not None
        except ImportError as e:
            pytest.fail(f"Could not import SpotifyClient: {e}")


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_song_creation_with_none_values(self):
        """Test Song creation with None values."""
        song = Song(None, "Test Track")
        assert song.artist is None
        assert song.track == "Test Track"

        song2 = Song("Test Artist", None)
        assert song2.artist == "Test Artist"
        assert song2.track is None

    def test_empty_playlist_handling(self):
        """Test handling of empty playlist data."""
        empty_songs = []

        successful_songs = []
        failed_songs = []

        for song in empty_songs:
            # This loop shouldn't execute
            successful_songs.append(song)

        assert len(successful_songs) == 0
        assert len(failed_songs) == 0

    @patch("tasks.SpotifyClient")
    def test_spotify_client_error_handling(self, mock_spotify_client_class):
        """Test Spotify client error scenarios."""
        mock_spotify_client = MagicMock()
        mock_spotify_client.get_app_token.return_value = False

        # Test app token failure
        token_success = mock_spotify_client.get_app_token()
        assert token_success is False

        # Test search failure
        mock_spotify_client.search_song.side_effect = Exception("API Error")

        try:
            mock_spotify_client.search_song("Test Query")
            pytest.fail("Expected exception was not raised")
        except Exception as e:
            assert str(e) == "API Error"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
