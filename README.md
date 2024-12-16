# ListenUP

A full-stack web application for transferring tracks from YouTube playlists to Spotify.

## Overview

**ListenUP** is a web application that allows users to transfer songs from their YouTube playlists to their Spotify libraries seamlessly. It integrates both the YouTube and Spotify APIs, enabling users to fetch, search, and add tracks to their Spotify accounts with ease.

## Features

- **Spotify Playlist Transfer**: Fetch tracks from your public YouTube playlists and add them to your Spotify library.
- **Playlist Management**: Search for tracks on Spotify and create or modify your personal playlists.
- **User Authentication**: Secure OAuth-based authentication for Spotify users to log in and manage their music collections.

## Tech Stack

- **Backend**: Python (Flask), Spotify API, YouTube Data API
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: OAuth 2.0 with Spotify

## Prerequisites

1. Python 3.7 or higher
2. Node.js
3. Spotify Developer Account
4. YouTube Data API v3 Credentials

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/esosaoh/ListenUP.git
cd ListenUP
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the backend directory:

```plaintext
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
```

### 4. Run the Backend

```bash
python backend/app.py
```

### 5. Setup Frontend

```bash
cd frontend
npm install
npm start
```

## Usage

1. Open the web application in your browser
2. Log in with your Spotify account
3. Select a YouTube playlist to transfer
4. Review and add tracks to your Spotify playlists

## Contributing

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/awesome-feature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some awesome feature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/awesome-feature
   ```
5. Open a Pull Request