# Playlifts

A full-stack web application for transferring tracks from YouTube playlists to Spotify.

## Overview

**Playlifts** is a web application that allows users to transfer songs from their YouTube playlists to their Spotify libraries seamlessly. It integrates both the YouTube and Spotify APIs, enabling users to fetch, search, and add tracks to their Spotify accounts with ease.

## Features

- **Spotify Playlist Transfer**: Fetch tracks from your public YouTube playlists and add them to your Spotify library
- **Playlist Management**: Search for tracks on Spotify and create or modify your personal playlists
- **User Authentication**: Secure OAuth-based authentication for Spotify users to log in and manage their music collections

## Tech Stack

- **Backend**: Python (Flask), MySQL, Spotify API, YouTube Data API
- **Frontend**: React.js, TypeScript, Tailwind CSS
- **Authentication**: OAuth 2.0 with Spotify
- **Containerization**: Docker, Docker Compose

## Prerequisites

- Docker and Docker Compose
- Spotify Developer Account
- YouTube Data API v3 Credentials

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/esosaoh/Playlifts.git
cd Playlifts
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```plaintext
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
```

### 3. Build and Run with Docker

```bash
# Build and start all services
docker-compose up --build

# To run in detached mode
docker-compose up -d
```

### 5. Access the application

1. Frontend: http://localhost:5173
2. Backend API: http://localhost:8889

## Usage

1. Open the web application in your browser
2. Log in with your Spotify account
3. Select a YouTube playlist to transfer
4. Review and add tracks to your Spotify playlists
