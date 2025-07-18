import { useIsLoggedIn } from './hooks/useIsLoggedIn'
import { Button } from './components/ui/Button'
import { Header } from './components/layout/Header'
import { PlaylistTransfer } from './components/features/PlaylistTransfer'
import { SpotifyToYouTubeTransfer } from './components/features/SpotifyToYouTubeTransfer'
import { PrivacyPolicy } from './components/pages/PrivacyPolicy'
import { TermsOfService } from './components/pages/TermsOfService'
import { motion } from 'framer-motion'
import { Music, Music2, Youtube } from 'lucide-react'
import { useEffect, useState, useLayoutEffect } from 'react'
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function LoginPage() {
  const [dark, setDark] = useState(true)
  const [isRetrying, setIsRetrying] = useState(false)
  
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])
  
  const handleSpotifyLogin = async () => {
    setIsRetrying(true)
    try {
      const res = await fetch('https://api.playlifts.com/spotify/login', { credentials: 'include' });
      const data = await res.json()
      window.location.href = data.auth_url
    } catch (error) {
      console.error('Login failed:', error)
      alert('Failed to start login process. Please check your connection and try again.')
    } finally {
      setIsRetrying(false)
    }
  }

  const handleYouTubeLogin = async () => {
    setIsRetrying(true)
    try {
      const res = await fetch('https://api.playlifts.com/youtube/login', { credentials: 'include' });
      const data = await res.json()
      window.location.href = data.auth_url
    } catch (error) {
      console.error('YouTube login failed:', error)
      alert('Failed to start YouTube login process. Please check your connection and try again.')
    } finally {
      setIsRetrying(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="text-center space-y-8 max-w-md"
      >
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-3xl shadow-2xl"
        >
          <Music className="w-10 h-10 text-white" />
        </motion.div>

        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white">
            Playlifts
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Transfer your music playlists between YouTube Music and Spotify seamlessly
          </p>
        </div>

        <div className="flex justify-center mb-4">
          <button
            aria-label="Toggle theme"
            onClick={() => setDark((d) => !d)}
            className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition shadow"
          >
            {dark ? (
              <SunIcon className="w-6 h-6 text-yellow-400" />
            ) : (
              <MoonIcon className="w-6 h-6 text-gray-600" />
            )}
          </button>
        </div>

        <div className="space-y-4">
          <Button
            onClick={handleSpotifyLogin}
            loading={isRetrying}
            size="lg"
            className="w-full text-lg py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg"
          >
            <Music2 className="w-5 h-5" />
            {isRetrying ? 'Connecting...' : 'Transfer YouTube → Spotify'}
          </Button>

          <Button
            onClick={handleYouTubeLogin}
            loading={isRetrying}
            size="lg"
            className="w-full text-lg py-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 shadow-lg"
          >
            <Youtube className="w-5 h-5" />
            {isRetrying ? 'Connecting...' : 'Transfer Spotify → YouTube'}
          </Button>
        </div>

        {/* Footer Links */}
        <div className="flex justify-center space-x-6 text-sm text-gray-500 dark:text-gray-400">
          <a href="/privacy-policy" className="hover:text-gray-700 dark:hover:text-gray-200 transition-colors">
            Privacy Policy
          </a>
          <a href="/terms" className="hover:text-gray-700 dark:hover:text-gray-200 transition-colors">
            Terms of Service
          </a>
        </div>
      </motion.div>
    </div>
  )
}

type TransferMode = 'youtube-to-spotify' | 'spotify-to-youtube'

function TransferApp({ loginStatus }: { loginStatus: any }) {
  const [transferMode, setTransferMode] = useState<TransferMode>('youtube-to-spotify')
  const [isRetrying, setIsRetrying] = useState(false)

  const handleSpotifyLogin = async () => {
    setIsRetrying(true)
    try {
      const res = await fetch('https://api.playlifts.com/spotify/login', { credentials: 'include' });
      const data = await res.json()
      window.location.href = data.auth_url
    } catch (error) {
      console.error('Spotify login failed:', error)
      alert('Failed to start Spotify login process. Please try again.')
    } finally {
      setIsRetrying(false)
    }
  }

  const handleYouTubeLogin = async () => {
    setIsRetrying(true)
    try {
      const res = await fetch('https://api.playlifts.com/youtube/login', { credentials: 'include' });
      const data = await res.json()
      window.location.href = data.auth_url
    } catch (error) {
      console.error('YouTube login failed:', error)
      alert('Failed to start YouTube login process. Please try again.')
    } finally {
      setIsRetrying(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      <main>
        {/* Transfer Mode Tabs */}
        <div className="container mx-auto px-4 pt-8">
          <div className="max-w-4xl mx-auto mb-8">
            <div className="flex bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-2 shadow-lg">
              <button
                onClick={() => setTransferMode('youtube-to-spotify')}
                className={`flex-1 flex items-center justify-center gap-3 py-4 px-6 rounded-xl font-semibold transition-all ${
                  transferMode === 'youtube-to-spotify'
                    ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-lg'
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                <Youtube className="w-5 h-5" />
                YouTube → Spotify
              </button>
              <button
                onClick={() => setTransferMode('spotify-to-youtube')}
                className={`flex-1 flex items-center justify-center gap-3 py-4 px-6 rounded-xl font-semibold transition-all ${
                  transferMode === 'spotify-to-youtube'
                    ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-lg'
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                <Music2 className="w-5 h-5" />
                Spotify → YouTube
              </button>
            </div>
          </div>
        </div>

        {/* Show login buttons for missing services above the transfer UI */}
        <div className="container mx-auto max-w-2xl mb-8">
          <div className="flex flex-col gap-4">
            {!loginStatus.spotify_logged_in && (
              <Button
                onClick={handleSpotifyLogin}
                loading={isRetrying}
                size="lg"
                className="w-full text-lg py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg"
              >
                <Music2 className="w-5 h-5" />
                {isRetrying ? 'Connecting...' : 'Login to Spotify'}
              </Button>
            )}
            {!loginStatus.youtube_logged_in && (
              <Button
                onClick={handleYouTubeLogin}
                loading={isRetrying}
                size="lg"
                className="w-full text-lg py-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 shadow-lg"
              >
                <Youtube className="w-5 h-5" />
                {isRetrying ? 'Connecting...' : 'Login to YouTube'}
              </Button>
            )}
          </div>
        </div>

        {/* Transfer Components */}
        {transferMode === 'youtube-to-spotify' ? (
          <PlaylistTransfer />
        ) : (
          <SpotifyToYouTubeTransfer />
        )}
      </main>
    </div>
  )
}

function AppContent() {
  useLayoutEffect(() => {
    document.documentElement.classList.add('dark');
  }, []);
  
  const loginStatus = useIsLoggedIn()

  useEffect(() => {
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => {
          caches.delete(name);
        });
      });
    }
  }, []);

  // If not logged into either service, show the initial login page
  if (loginStatus === null) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300">Checking login status...</p>
        </div>
      </div>
    )
  }

  if (!loginStatus.spotify_logged_in && !loginStatus.youtube_logged_in) {
    return <LoginPage />
  }

  // If logged into at least one service, show the transfer app (it will show login buttons for missing services as needed)
  return <TransferApp loginStatus={loginStatus} />
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="/terms" element={<TermsOfService />} />
        <Route path="*" element={<AppContent />} />
      </Routes>
    </Router>
  )
}

export default App
