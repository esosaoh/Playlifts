import React from 'react'

interface ProgressBarProps {
  value: number // 0-100
  label?: string
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ value, label }) => (
  <div className="w-full">
    {label && <span className="block mb-1 text-sm">{label}</span>}
    <div className="w-full bg-gray-200 rounded h-3">
      <div
        className="bg-green-600 h-3 rounded transition-all"
        style={{ width: `${value}%` }}
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={100}
        role="progressbar"
      />
    </div>
  </div>
)
