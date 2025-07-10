import React from 'react'

interface ProgressBarProps {
  value: number // 0-100
  label?: string
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ value, label }) => (
  <div className="w-full">
    <div className="flex justify-between items-center mb-2">
      {label && <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</span>}
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{Math.round(value)}%</span>
    </div>
    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
      <div
        className="bg-gradient-to-r from-green-500 to-emerald-600 h-3 rounded-full transition-all duration-500 ease-out shadow-sm"
        style={{ 
          width: `${Math.max(value, 0.5)}%`,
          minWidth: value > 0 ? '4px' : '0px'
        }}
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={100}
        role="progressbar"
      />
    </div>
  </div>
)
