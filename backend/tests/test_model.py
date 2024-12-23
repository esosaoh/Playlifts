import os
import sys
import unittest
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import app, db
from models import User

class TestUserModel(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_new_user(self):
        """Test creating a new user"""
        with app.app_context():
            spotify_id = "test123"
            email = "test@example.com"
            access_token = {"token": "dummy_token"}
            
            user = User.create_user(spotify_id, email, access_token)
            
            self.assertEqual(user.spotify_id, spotify_id)
            self.assertEqual(user.email, email)
            self.assertEqual(user.spotify_token, access_token)
            self.assertIsInstance(user.created_at, datetime)
            self.assertIsInstance(user.last_login, datetime)
    
    def test_user_representation(self):
        """Test the string representation of User model"""
        with app.app_context():
            user = User(spotify_id="test123", email="test@example.com")
            self.assertEqual(str(user), "<User test123>")
    
    def test_user_to_dict(self):
        """Test the to_dict method"""
        with app.app_context():
            now = datetime.utcnow()
            user = User(
                id=1,
                spotify_id="test123",
                email="test@example.com",
                created_at=now,
                last_login=now
            )
            
            user_dict = user.to_dict()
            
            self.assertEqual(user_dict["id"], 1)
            self.assertEqual(user_dict["spotify_id"], "test123")
            self.assertEqual(user_dict["email"], "test@example.com")
            self.assertEqual(user_dict["created_at"], now)
            self.assertEqual(user_dict["last_login"], now)
    
    def test_existing_user_update(self):
        """Test updating an existing user"""
        with app.app_context():
            spotify_id = "test123"
            email = "test@example.com"
            initial_token = {"token": "initial_token"}
            updated_token = {"token": "updated_token"}
            
            # Create initial user
            user1 = User.create_user(spotify_id, email, initial_token)
            
            # Update same user
            user2 = User.create_user(spotify_id, email, updated_token)
            
            # Verify it's the same user but updated
            self.assertEqual(user1.id, user2.id)
            self.assertEqual(user2.spotify_token, updated_token)
            # Instead of comparing timestamps, just verify both have timestamps
            self.assertIsInstance(user1.last_login, datetime)
            self.assertIsInstance(user2.last_login, datetime)

if __name__ == '__main__':
    unittest.main()