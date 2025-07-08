import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'

export const Header = () => {
  const [dark, setDark] = useState(false)

  const toggleTheme = () => {
    setDark(!dark)
    document.documentElement.classList.toggle('dark', !dark)
  }

  return (
    <header className="flex items-center justify-between px-8 py-4 bg-white dark:bg-gray-900 shadow-md rounded-b-2xl">
      <div className="flex items-center gap-2">
        <span className="text-2xl font-extrabold text-green-600 tracking-tight">
          ListenUP
        </span>
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
    </header>
  )
}
