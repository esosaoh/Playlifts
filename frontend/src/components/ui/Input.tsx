import React from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
}

export const Input: React.FC<InputProps> = ({ label, error, ...props }) => (
  <div className="mb-4">
    <label className="block text-sm font-medium mb-1" htmlFor={props.id}>
      {label}
    </label>
    <input
      className={`w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 ${
        error
          ? 'border-red-500 focus:ring-red-400'
          : 'border-gray-300 focus:ring-green-400'
      }`}
      {...props}
    />
    {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
  </div>
)
