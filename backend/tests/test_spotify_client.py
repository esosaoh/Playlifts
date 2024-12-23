import unittest
from unittest.mock import patch, Mock
from spotify_client import SpotifyClient

class TestSpotifyClient(unittest.TestCase):
    def setUp(self):
        self.api_token = "dummy_token"
        self.spotify_client = SpotifyClient(self.api_token)
        
        # Sample response for successful search
        self.sample_search_response = {
            "tracks": {
                "items": [
                    {
                        "id": "3AJwUDP919kvQ9QcozQPxg",
                        "name": "Viva La Vida",
                        "artists": [{"name": "Coldplay"}]
                    }
                ]
            }
        }
        
    @patch('requests.get')
    def test_search_song_success(self, mock_get):
        """Test successful song search"""
        mock_response = Mock()
        mock_response.json.return_value = self.sample_search_response
        mock_get.return_value = mock_response
        
        song_id = self.spotify_client.search_song("Coldplay", "Viva la Vida")
        self.assertEqual(song_id, "3AJwUDP919kvQ9QcozQPxg")
        
    @patch('requests.get')
    def test_search_song_no_results(self, mock_get):
        """Test song search with no results"""
        mock_response = Mock()
        mock_response.json.return_value = {"tracks": {"items": []}}
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            self.spotify_client.search_song("NonExistent", "Artist")
        
    @patch('requests.put')
    def test_add_song_to_spotify(self, mock_put):
        """Test adding song to Spotify"""
        mock_response = Mock()
        mock_response.ok = True
        mock_put.return_value = mock_response
        
        result = self.spotify_client.add_song_to_spotify("test_song_id")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()