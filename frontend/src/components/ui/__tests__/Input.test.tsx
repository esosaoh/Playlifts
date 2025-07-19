import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Input } from '../Input'

describe('Input', () => {
  it('renders input with label and placeholder', () => {
    render(<Input label="Test Input" placeholder="Enter text" />)
    expect(screen.getByText('Test Input')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument()
  })

  it('renders input with value', () => {
    render(<Input label="Test Input" value="test value" onChange={() => {}} />)
    const input = screen.getByDisplayValue('test value')
    expect(input).toBeInTheDocument()
  })

  it('handles onChange events', () => {
    const handleChange = vi.fn()
    render(<Input label="Test Input" onChange={handleChange} />)
    
    const input = screen.getByRole('textbox')
    input.setAttribute('value', 'new value')
    input.dispatchEvent(new Event('input', { bubbles: true }))
    
    expect(handleChange).toHaveBeenCalled()
  })

  it('applies custom className', () => {
    render(<Input label="Test Input" className="custom-input" />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveClass('custom-input')
  })

  it('supports different input types', () => {
    render(<Input label="Email" type="email" placeholder="Email" />)
    const input = screen.getByPlaceholderText('Email')
    expect(input).toHaveAttribute('type', 'email')
  })

  it('can be disabled', () => {
    render(<Input label="Test Input" disabled />)
    const input = screen.getByRole('textbox')
    expect(input).toBeDisabled()
  })

  it('shows error message when error prop is provided', () => {
    render(<Input label="Test Input" error="This field is required" />)
    expect(screen.getByText('This field is required')).toBeInTheDocument()
  })

  it('applies error styling when error is present', () => {
    render(<Input label="Test Input" error="Error message" />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveClass('border-red-500')
  })

  it('associates label with input using htmlFor', () => {
    render(<Input label="Test Input" id="test-input" />)
    const label = screen.getByText('Test Input')
    const input = screen.getByRole('textbox')
    
    expect(label).toHaveAttribute('for', 'test-input')
    expect(input).toHaveAttribute('id', 'test-input')
  })
}) 