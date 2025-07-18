import { useEffect, useState } from 'react'

interface LoginStatus {
  spotify_logged_in: boolean
  youtube_logged_in: boolean
  both_logged_in: boolean
}

export function useIsLoggedIn() {
  const [loginStatus, setLoginStatus] = useState<LoginStatus | null>(null)

  useEffect(() => {
    const checkLogin = async () => {
      try {
        const timestamp = Date.now()
        const response = await fetch(`https://api.playlifts.com/auth/check?t=${timestamp}`, { 
          credentials: 'include',
          signal: AbortSignal.timeout(5000)
        })
        
        if (response.ok) {
          const data = await response.json()
          setLoginStatus(data)
        } else {
          console.warn('Login check failed with status:', response.status)
          setLoginStatus({
            spotify_logged_in: false,
            youtube_logged_in: false,
            both_logged_in: false
          })
        }
      } catch (error) {
        console.error('Error checking login status:', error)
        setLoginStatus({
          spotify_logged_in: false,
          youtube_logged_in: false,
          both_logged_in: false
        })
      }
    }

    checkLogin()
  }, [])

  return loginStatus
}
