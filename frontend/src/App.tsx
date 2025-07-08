import { useState, useEffect } from 'react'

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    checkLoginStatus()
  }, [])

  const checkLoginStatus = async () => {
    try {
      const response = await fetch('http://localhost:8889/check_login', {
        credentials: 'include',
      })
      if (response.ok) {
        const data = await response.json()
        setIsLoggedIn(data.is_logged_in)
      }
    } catch (error) {
      console.error('Failed to check login status:', error)
    }
  }
  const handleSpotifyLogin = async () => {
    try {
      const response = await fetch('http://localhost:8889/login')
      if (response.ok) {
        const data = await response.json()
        window.location.href = data.auth_url
      }
    } catch (error) {
      console.error('Login failed:', error)
    }
  }

  const handleSubmitPlaylist = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      const response = await fetch('http://localhost:8889/process-youtube', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: youtubeUrl }),
        credentials: 'include',
      })
      if (response.ok) {
        alert('Playlist transferred successfully!')
        setYoutubeUrl('')
      }
    } catch (error) {
      console.error('Processing failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-4">ListenUp</h1>

        <p className="text-gray-600 mb-8 text-center">
          Transfer songs from your favorite YouTube playlists to Spotify with
          just one click. Login with Spotify to get started!
        </p>

        {!isLoggedIn ? (
          <button
            onClick={handleSpotifyLogin}
            className="w-full bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition"
          >
            Login with Spotify
          </button>
        ) : (
          <form onSubmit={handleSubmitPlaylist} className="space-y-4">
            <div>
              <label
                htmlFor="playlist"
                className="block text-sm font-medium text-gray-700"
              >
                YouTube Playlist URL
              </label>
              <input
                id="playlist"
                type="text"
                value={youtubeUrl}
                onChange={e => setYoutubeUrl(e.target.value)}
                placeholder="Paste your YouTube playlist URL here"
                className="mt-1 block w-full rounded border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition"
            >
              Convert Playlist
            </button>
          </form>
        )}
      </div>
    </div>
  )
}

export default App
