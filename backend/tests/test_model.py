from flask import session
from app import app, db
from spotify_client import SpotifyClient
from models import User

def test_user_creation(test_db):
    """Test creating a new user"""
    user = User.create_user(
        spotify_id="test123",
        email="test@test.com",
        access_token={"token": "test_token"}
    )
    
    assert user.spotify_id == "test123"
    assert user.email == "test@test.com"
    assert user.spotify_token == {"token": "test_token"}
    assert user.last_login is not None

def test_user_duplicate_creation(test_db):
    """Test creating a duplicate user updates existing user"""
    # Create initial user
    user1 = User.create_user(
        spotify_id="test123",
        email="test@test.com",
        access_token={"token": "test_token1"}
    )
    
    # Create duplicate user
    user2 = User.create_user(
        spotify_id="test123",
        email="test@test.com",
        access_token={"token": "test_token2"}
    )
    
    assert user1.id == user2.id
    assert user2.spotify_token == {"token": "test_token2"}

def test_user_to_dict(test_db):
    """Test user to_dict method"""
    user = User.create_user(
        spotify_id="test123",
        email="test@test.com",
        access_token={"token": "test_token"}
    )
    
    user_dict = user.to_dict()
    assert user_dict["spotify_id"] == "test123"
    assert user_dict["email"] == "test@test.com"
    assert "spotify_token" not in user_dict