"""
Playlifts Backend Package

A Flask-based backend service for transferring playlists between Spotify and YouTube Music.

Author: esosaoh
Version: 1.0.0
Description: Backend API for the Playlifts playlist transfer application
"""

__version__ = "1.0.0"
__author__ = "esosaoh"
__description__ = "Backend API for the Playlifts playlist transfer application"
__url__ = "https://github.com/esosaoh/Playlifts"

# Package imports
from .app import app
from .models import *
from .spotify_client import SpotifyClient
from .youtube_client import YouTubeClient

__all__ = [
    "app",
    "SpotifyClient",
    "YouTubeClient",
]
