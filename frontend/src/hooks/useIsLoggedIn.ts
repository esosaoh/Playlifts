import { useEffect, useState } from 'react'

export function useIsLoggedIn() {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null)

  useEffect(() => {
    fetch('http://localhost:8889/check_login', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setIsLoggedIn(data.is_logged_in))
      .catch(() => setIsLoggedIn(false))
  }, [])

  return isLoggedIn
}
