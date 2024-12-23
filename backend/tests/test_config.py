import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import app

class TestConfig(unittest.TestCase):
    def test_app_configuration(self):
        """Test basic Flask app configuration"""
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'].startswith('mysql+pymysql'))
        self.assertTrue(app.config['SECRET_KEY'] is not None)
        
    def test_cors_enabled(self):
        """Test that CORS is enabled"""
        self.assertTrue('Access-Control-Allow-Origin' in app.test_client().options('/').headers)

if __name__ == '__main__':
    unittest.main()
