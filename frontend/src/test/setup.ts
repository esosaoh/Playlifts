import '@testing-library/jest-dom'
import { vi } from 'vitest'

vi.stubGlobal('fetch', vi.fn())

Object.defineProperty(window, 'location', {
  value: {
    href: 'http://localhost:3000',
    reload: vi.fn(),
  },
  writable: true,
}) 