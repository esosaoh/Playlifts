import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Header } from '../Header'

// Mock react-router-dom
vi.mock('react-router-dom', () => ({
  Link: ({ children, to, ...props }: any) => <a href={to} {...props}>{children}</a>
}))

describe('Header', () => {
  it('renders the Playlifts logo', () => {
    render(<Header />)
    expect(screen.getByText('Playlifts')).toBeInTheDocument()
  })

  it('renders theme toggle button', () => {
    render(<Header />)
    expect(screen.getByLabelText(/toggle theme/i)).toBeInTheDocument()
  })

  it('renders logout button', () => {
    render(<Header />)
    expect(screen.getByLabelText(/logout/i)).toBeInTheDocument()
  })

  it('renders privacy and terms links', () => {
    render(<Header />)
    expect(screen.getByText('Privacy Policy')).toBeInTheDocument()
    expect(screen.getByText('Terms of Service')).toBeInTheDocument()
  })

  it('logo links to home page', () => {
    render(<Header />)
    const logoLink = screen.getByText('Playlifts').closest('a')
    expect(logoLink).toHaveAttribute('href', '/')
  })

  it('privacy link goes to privacy policy', () => {
    render(<Header />)
    const privacyLink = screen.getByText('Privacy Policy')
    expect(privacyLink).toHaveAttribute('href', '/privacy-policy')
  })

  it('terms link goes to terms page', () => {
    render(<Header />)
    const termsLink = screen.getByText('Terms of Service')
    expect(termsLink).toHaveAttribute('href', '/terms')
  })
}) 