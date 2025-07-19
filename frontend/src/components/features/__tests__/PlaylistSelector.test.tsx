import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { PlaylistSelector } from '../PlaylistSelector'

const mockFetch = vi.fn()

describe('PlaylistSelector', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.stubGlobal('fetch', mockFetch)
  })

  it('renders loading state initially', () => {
    mockFetch.mockImplementation(() => new Promise(() => {})) // Never resolves
    
    render(
      <PlaylistSelector 
        onPlaylistSelect={vi.fn()} 
        selectedPlaylistId={null}
      />
    )
    
    expect(screen.getByText(/loading playlists/i)).toBeInTheDocument()
  })

  it('renders playlists when fetch succeeds', async () => {
    const mockPlaylists = [
      {
        id: '1',
        name: 'My Playlist',
        tracks_count: 10,
        owner: 'me',
        public: true,
        cover_image: null
      }
    ]

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ playlists: mockPlaylists })
    })

    render(
      <PlaylistSelector 
        onPlaylistSelect={vi.fn()} 
        selectedPlaylistId={null}
      />
    )

    await waitFor(() => {
      expect(screen.getByText('My Playlist')).toBeInTheDocument()
    })
  })

  it('renders error when fetch fails', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    })

    render(
      <PlaylistSelector 
        onPlaylistSelect={vi.fn()} 
        selectedPlaylistId={null}
      />
    )

    await waitFor(() => {
      expect(screen.getByText(/failed to load playlists/i)).toBeInTheDocument()
    })
  })

  it('shows Spotify login button when session expires', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 401
    })

    const onSpotifyLogin = vi.fn()

    render(
      <PlaylistSelector 
        onPlaylistSelect={vi.fn()} 
        selectedPlaylistId={null}
        onSpotifyLogin={onSpotifyLogin}
      />
    )

    await waitFor(() => {
      expect(screen.getByText(/your spotify session has expired/i)).toBeInTheDocument()
      expect(screen.getByText(/login to spotify/i)).toBeInTheDocument()
    })
  })

  it('calls onPlaylistSelect when playlist is clicked', async () => {
    const mockPlaylists = [
      {
        id: '1',
        name: 'My Playlist',
        tracks_count: 10,
        owner: 'me',
        public: true,
        cover_image: null
      }
    ]

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ playlists: mockPlaylists })
    })

    const onPlaylistSelect = vi.fn()

    render(
      <PlaylistSelector 
        onPlaylistSelect={onPlaylistSelect} 
        selectedPlaylistId={null}
      />
    )

    await waitFor(() => {
      screen.getByText('My Playlist').click()
    })

    expect(onPlaylistSelect).toHaveBeenCalledWith('1', 'My Playlist', null)
  })
}) 