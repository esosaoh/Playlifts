import { motion } from 'framer-motion'

export const SongPreview = ({ song }: { song: any }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3, ease: 'easeOut' }}
    className="flex items-center gap-4 p-4 rounded-2xl bg-gray-50 dark:bg-gray-800 mb-2 shadow-md border border-gray-100 dark:border-gray-700"
  >
    {/* Placeholder for artwork */}
    <div className="w-14 h-14 bg-gray-200 dark:bg-gray-700 rounded-xl flex items-center justify-center text-gray-400 text-xl font-bold">
      ♫
    </div>
    <div className="flex-1 min-w-0">
      <div className="font-semibold text-lg text-gray-900 dark:text-white truncate">
        {song.track}
      </div>
      <div className="text-sm text-gray-500 dark:text-gray-300 truncate">
        {song.artist}
      </div>
      {song.status === 'failed' && (
        <div className="text-xs text-red-500 mt-1">Failed: {song.reason}</div>
      )}
    </div>
    <div>
      {song.status === 'success' ? (
        <span className="text-green-600 font-bold text-2xl">✓</span>
      ) : (
        <span className="text-red-600 font-bold text-2xl">✗</span>
      )}
    </div>
  </motion.div>
)
