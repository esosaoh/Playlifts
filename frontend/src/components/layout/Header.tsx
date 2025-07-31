import { SunIcon, MoonIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'
import { Link } from 'react-router-dom'

export const Header = () => {
  const [dark, setDark] = useState(false)

  const toggleTheme = () => {
    setDark(!dark)
    document.documentElement.classList.toggle('dark', !dark)
  }

  const handleLogout = async () => {
    try {
      await fetch('https://api.playlifts.com/auth/logout', {
        method: 'POST',
        credentials: 'include'
      })  
      window.location.reload()
    } catch (error) {
      console.error('Logout failed:', error)
      window.location.reload()
    }
  }

  return (
    <header className="flex items-center justify-between px-8 py-4 bg-white dark:bg-gray-900 shadow-md rounded-b-2xl">
      <div className="flex items-center gap-2">
        <Link to="/" className="text-2xl font-extrabold text-green-600 tracking-tight hover:text-green-700 transition-colors">
          Playlifts
        </Link>
      </div>
      <div className="flex items-center gap-4">
        {/* Footer Links */}
        <div className="flex space-x-4 text-sm text-gray-600 dark:text-gray-400">
          <a href="https://playlifts.com/privacy-policy" className="hover:text-gray-800 dark:hover:text-gray-200 transition-colors">
            Privacy Policy
          </a>
          <a href="https://playlifts.com/terms" className="hover:text-gray-800 dark:hover:text-gray-200 transition-colors">
            Terms of Service
          </a>
        </div>
        <button
          aria-label="Toggle theme"
          onClick={toggleTheme}
          className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition shadow"
        >
          {dark ? (
            <SunIcon className="w-6 h-6 text-yellow-400" />
          ) : (
            <MoonIcon className="w-6 h-6 text-gray-600" />
          )}
        </button>
        <button
          aria-label="Logout"
          onClick={handleLogout}
          className="p-2 rounded-full bg-red-100 dark:bg-red-900/20 hover:bg-red-200 dark:hover:bg-red-900/40 transition shadow text-red-600 dark:text-red-400"
        >
          <ArrowRightOnRectangleIcon className="w-6 h-6" />
        </button>
      </div>
    </header>
  )
}
