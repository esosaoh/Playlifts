import { useState } from 'react'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { ProgressBar } from '../ui/ProgressBar'
import { SongPreview } from './SongPreview'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/Card'
import { motion } from 'framer-motion'
import { Music, Youtube, Music2 } from 'lucide-react'

export const PlaylistTransfer = () => {
  const [url, setUrl] = useState('')
  const [isTransferring, setIsTransferring] = useState(false)
  const [progress, setProgress] = useState(0)
  const [songs, setSongs] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleTransfer = async () => {
    setIsTransferring(true)
    setError(null)
    setSongs([])
    setProgress(0)

    try {
      const res = await fetch('http://localhost:8889/process-youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
        credentials: 'include',
      })
      const data = await res.json()

      if (res.ok) {
        const allSongs = [
          ...data.success.songs.map((s: any) => ({ ...s, status: 'success' })),
          ...data.failed.songs.map((s: any) => ({
            ...s,
            status: 'failed',
            reason: s.reason,
          })),
        ]
        setSongs(allSongs)
        setProgress(100)
      } else {
        setError(data.error || 'Transfer failed.')
      }
    } catch (e: any) {
      setError(e.message || 'Unknown error')
    } finally {
      setIsTransferring(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="max-w-2xl mx-auto"
        >
          {/* Hero Section */}
          <div className="text-center mb-12">
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl mb-6 shadow-lg"
            >
              <Music className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Transfer Your Music
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-lg mx-auto">
              Seamlessly move your YouTube playlists to Spotify with our
              intelligent transfer system
            </p>
          </div>

          {/* Main Transfer Card */}
          <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
            <CardHeader className="text-center pb-4">
              <CardTitle className="text-2xl font-bold text-gray-900 dark:text-white">
                YouTube to Spotify Transfer
              </CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-300">
                Paste your YouTube playlist URL below to get started
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <Input
                  label="YouTube Playlist URL"
                  value={url}
                  onChange={e => setUrl(e.target.value)}
                  placeholder="https://www.youtube.com/playlist?list=..."
                  disabled={isTransferring}
                  className="text-lg"
                />
                <Button
                  onClick={handleTransfer}
                  loading={isTransferring}
                  disabled={!url}
                  size="lg"
                  className="w-full text-lg py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg"
                >
                  <Youtube className="w-5 h-5" />
                  Transfer to Spotify
                  <Music2 className="w-5 h-5" />
                </Button>
              </div>

              {isTransferring && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="space-y-4"
                >
                  <ProgressBar value={progress} label="Transferring songs..." />
                  <div className="text-center text-sm text-gray-600 dark:text-gray-300">
                    Processing your playlist...
                  </div>
                </motion.div>
              )}

              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300 text-center"
                >
                  {error}
                </motion.div>
              )}

              {songs.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-3"
                >
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Transfer Results
                  </h3>
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {songs.map((song, idx) => (
                      <SongPreview key={idx} song={song} />
                    ))}
                  </div>
                </motion.div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
