import { useEffect, useState } from 'react'

export function useIsLoggedIn() {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null)

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
          setIsLoggedIn(data.is_logged_in)
        } else {
          console.warn('Login check failed with status:', response.status)
          setIsLoggedIn(false)
        }
      } catch (error) {
        console.error('Error checking login status:', error)
        setIsLoggedIn(false)
      }
    }

    checkLogin()
  }, [])

  return isLoggedIn
}
