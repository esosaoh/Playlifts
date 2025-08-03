# Backend tests package
# This package contains comprehensive tests for the Playlifts backend

"""
Backend Tests Package

This package contains comprehensive tests for the Playlifts backend application.
The tests are organized by component and cover:

- Flask app routes and endpoints (test_app.py)
- Celery tasks and asynchronous processing (test_tasks.py)
- Database models and operations (test_models.py)
- Configuration and environment setup (test_config.py)
- Spotify API client functionality (test_spotify_client.py)
- YouTube API client functionality (test_youtube_client.py)

Test Categories:
- Unit tests: Test individual components in isolation
- Integration tests: Test component interactions
- API tests: Test HTTP endpoints and responses

Usage:
    # Run all tests
    pytest backend/tests/

    # Run specific test file
    pytest backend/tests/test_app.py

    # Run tests with coverage
    pytest backend/tests/ --cov=backend --cov-report=html

    # Run only unit tests
    pytest backend/tests/ -m unit

    # Run only integration tests
    pytest backend/tests/ -m integration

    # Run only API tests
    pytest backend/tests/ -m api

    # Skip slow tests
    pytest backend/tests/ -m "not slow"
"""

__version__ = "1.0.0"
__author__ = "esosaoh"
