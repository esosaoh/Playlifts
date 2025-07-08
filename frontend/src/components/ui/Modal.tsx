import React, { useEffect, useRef } from 'react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
}) => {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      ref.current?.focus()
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      tabIndex={-1}
      ref={ref}
      onKeyDown={e => e.key === 'Escape' && onClose()}
    >
      <div className="bg-white dark:bg-gray-900 rounded shadow-lg p-6 w-full max-w-md">
        <h2 id="modal-title" className="text-lg font-bold mb-4">
          {title}
        </h2>
        {children}
        <button
          className="mt-4 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </div>
  )
}
