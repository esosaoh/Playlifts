# Playlifts Backend Documentation
This document outlines the backend services, API endpoints, background tasks, and core logic for Playlifts.  

## Environment Variables
Required variables (from `.env`):  
```python
SECRET_KEY= # flask app's secret key
FRONTEND_URL=https://playlifts.com
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
YOUTUBE_API_KEY=
```

## Session & Security
- Session stored in Flask session cookies.
- Cookies configured with:
  - SameSite=None
  - Secure=True
- Tokens handled server-side, never exposed to frontend.

## Base URL
```bash
https://api.playlifts.com
```

# Endpoints

## 1. Health Check

**GET** `/healthz`

**Response:**
```json
{ "status": "ok" }
```

---

## 2. Authentication

### Spotify Login

**GET** `/spotify/login`

**Response:**
```json
{ "auth_url": "<Spotify OAuth URL>" }
```

### Spotify Callback

**GET** `/spotify/callback`

Sets session tokens and redirects to `FRONTEND_URL`.

---

### YouTube Login

**GET** `/youtube/login`

**Response:**
```json
{ "auth_url": "<Google OAuth URL>" }
```

### YouTube Callback

**GET** `/youtube/callback`

Sets session tokens and redirects to `FRONTEND_URL`.

---

### Check Auth Status

**GET** `/auth/check`

**Response:**
```json
{
  "spotify_logged_in": true/false,
  "youtube_logged_in": true/false,
  "both_logged_in": true/false
}
```

---

### Logout

**POST** `/auth/logout`

Clears session and deletes cookies.

---

## 3. Spotify

### Get Playlists

**GET** `/spotify/playlists`

**Headers:** Session with Spotify token

**Response:**
```json
{
  "playlists": [
    { "id": "...", "name": "...", "tracks_count": 50, "owner": "...", "public": true/false, "cover_image": "..." }
  ]
}
```

---

### Transfer Spotify → YouTube

**POST** `/spotify/transfer`

**Body:**
```json
{
  "spotify_playlist_id" or "spotify_url": "...",
  "youtube_playlist_id": "..."
}
```

**Response:**
```json
{ "task_id": "<celery-task-id>" }
```

---

## 4. YouTube

### Get Playlists

**GET** `/youtube/playlists`

**Response:**
```json
{ "playlists": [ { "id": "...", "title": "..." } ] }
```

---

### Transfer YouTube → Spotify

**POST** `/youtube/transfer`

**Body:**
```json
{
  "url": "<YouTube Playlist URL>",
  "playlist_id": "<Spotify Playlist ID or null>"
}
```

**Response:**
```json
{ "task_id": "<celery-task-id>" }
```

---

## 5. Task Status

**GET** `/tasks/status/<task_id>`

**Response:**
```json
{
  "state": "PENDING|PROGRESS|SUCCESS|FAILURE",
  "progress": 0-100,
  "status": "...",
  "result" or "error": {...}
}
```

---

## Background Tasks

### YouTube → Spotify (`transfer_playlist_task`)

- Fetches songs from YouTube playlist.
- Searches for songs on Spotify.
- Adds to target Spotify playlist or Liked Songs.
- Reports progress every few tracks.

### Spotify → YouTube (`transfer_spotify_to_youtube_task`)

- Fetches up to 15 tracks from Spotify playlist (using Client Credentials for public access).
- Searches for videos on YouTube.
- Adds to target YouTube playlist.

---

## Key Utilities

### SpotifyClient
Handles token-based and app-only authentication.  
**Methods:**
- `get_tracks_from_playlist()`
- `search_song()`
- `add_song_to_playlist()`
- `add_song_to_spotify()`

### YouTubeClient
Handles playlist fetch, search, and video insertion.  
**Methods:**
- `get_videos_from_playlist()`
- `get_playlists()`
- `search_videos()`
- `add_video_to_playlist()`

---

