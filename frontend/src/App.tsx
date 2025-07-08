import { useIsLoggedIn } from './hooks/useIsLoggedIn'
import { Button } from './components/ui/Button'
import { Header } from './components/layout/Header'
import { PlaylistTransfer } from './components/features/PlaylistTransfer'
import { motion } from 'framer-motion'
import { Music, Music2 } from 'lucide-react'

function LoginPage() {
  const handleLogin = async () => {
    const res = await fetch('http://localhost:8889/login')
    const data = await res.json()
    window.location.href = data.auth_url
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
            ListenUP
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Transfer your YouTube playlists to Spotify seamlessly
          </p>
        </div>

        <Button
          onClick={handleLogin}
          size="lg"
          className="w-full text-lg py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg"
        >
          <Music2 className="w-5 h-5" />
          Login with Spotify
        </Button>
      </motion.div>
    </div>
  )
}

function App() {
  const isLoggedIn = useIsLoggedIn()

  if (isLoggedIn === null) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    )
  }

  if (!isLoggedIn) return <LoginPage />

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      <main>
        <PlaylistTransfer />
      </main>
    </div>
  )
}

export default App
