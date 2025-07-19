import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../Card'

describe('Card', () => {
  it('renders card with content', () => {
    render(
      <Card>
        <CardContent>Card content</CardContent>
      </Card>
    )
    expect(screen.getByText('Card content')).toBeInTheDocument()
  })

  it('renders card with header', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>Card content</CardContent>
      </Card>
    )
    
    expect(screen.getByText('Card Title')).toBeInTheDocument()
    expect(screen.getByText('Card Description')).toBeInTheDocument()
    expect(screen.getByText('Card content')).toBeInTheDocument()
  })

  it('applies custom className', () => {
    render(
      <Card className="custom-class">
        <CardContent>Content</CardContent>
      </Card>
    )
    
    const card = screen.getByText('Content').closest('[data-slot="card"]')
    expect(card).toHaveClass('custom-class')
  })
}) 