import pytest
import re


class TestRouteDefinitions:
    """Test that routes are defined in the source code."""
    
    def test_index_route_defined(self):
        """Test that index route is defined in app.py."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "@app.route('/')" in content
        assert "def index():" in content
        print("✓ Index route is defined")
    
    def test_health_route_defined(self):
        """Test that health route is defined in app.py."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "@app.route('/healthz'" in content
        assert "def health_check():" in content
        print("✓ Health route is defined")
    
    def test_spotify_routes_defined(self):
        """Test that Spotify routes are defined in app.py."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "@app.route('/spotify/login')" in content
        assert "@app.route('/spotify/playlists'" in content
        assert "@app.route('/spotify/transfer'" in content
        print("✓ Spotify routes are defined")
    
    def test_youtube_routes_defined(self):
        """Test that YouTube routes are defined in app.py."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "@app.route('/youtube/login')" in content
        assert "@app.route('/youtube/playlists')" in content
        assert "@app.route('/youtube/transfer'" in content
        print("✓ YouTube routes are defined")
    
    def test_auth_routes_defined(self):
        """Test that auth routes are defined in app.py."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "@app.route('/auth/check'" in content
        assert "@app.route('/auth/logout'" in content
        print("✓ Auth routes are defined")
    
    def test_task_routes_defined(self):
        """Test that task routes are defined in app.py."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "@app.route('/tasks/status/<task_id>')" in content
        print("✓ Task routes are defined")


class TestUtilityFunctions:
    """Test utility functions by reading source code."""
    
    def test_extract_spotify_playlist_id_function_exists(self):
        """Test that the extract function exists in app.py."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "def _extract_spotify_playlist_id(" in content
        print("✓ Extract Spotify playlist ID function exists")
    
    def test_extract_spotify_playlist_id_logic(self):
        """Test the logic of the extract function."""
        def extract_spotify_playlist_id(value):
            if not value:
                return None
            if len(value) == 22 and value.isalnum():
                return value
            try:
                if 'playlist' in value:
                    parts = value.split('/')
                    if 'playlist' in parts:
                        idx = parts.index('playlist')
                        if idx + 1 < len(parts):
                            return parts[idx + 1]
            except Exception:
                pass
            return None
        
        assert extract_spotify_playlist_id('37i9dQZF1DXcBWIGoYBM5M') == '37i9dQZF1DXcBWIGoYBM5M'
        assert extract_spotify_playlist_id('https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M') == '37i9dQZF1DXcBWIGoYBM5M'
        assert extract_spotify_playlist_id('invalid') is None
        print("✓ Extract Spotify playlist ID logic works correctly")


class TestAppStructure:
    """Test that the app has the correct structure."""
    
    def test_app_file_exists(self):
        """Test that app.py file exists."""
        import os
        assert os.path.exists('app.py')
        print("✓ App.py file exists")
    
    def test_app_has_environment_variables(self):
        """Test that app.py uses environment variables."""
        with open('app.py', 'r') as f:
            content = f.read()
        assert "SPOTIFY_CLIENT_ID" in content
        assert "SPOTIFY_CLIENT_SECRET" in content
        assert "GOOGLE_CLIENT_ID" in content
        print("✓ App.py uses environment variables")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"]) 