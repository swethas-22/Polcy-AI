import React from 'react';

export default function BuildingGraphic({ className = "" }) {
  return (
    <svg 
      viewBox="0 0 300 90" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={`w-full opacity-20 pointer-events-none select-none ${className}`}
    >
      {/* Central Dome */}
      <path d="M150 15C138 15 130 25 130 35H170C170 25 162 15 150 15Z" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="150" y1="5" x2="150" y2="15" stroke="#90A4AE" strokeWidth="1.5" />
      {/* Center pediment & columns */}
      <polygon points="120,40 180,40 150,28" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="125" y1="40" x2="125" y2="75" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="137" y1="40" x2="137" y2="75" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="150" y1="40" x2="150" y2="75" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="163" y1="40" x2="163" y2="75" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="175" y1="40" x2="175" y2="75" stroke="#90A4AE" strokeWidth="1.5" />
      <rect x="120" y="75" width="60" height="10" stroke="#90A4AE" strokeWidth="1.5" />

      {/* Left Wing */}
      <rect x="30" y="45" width="90" height="30" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="45" y1="50" x2="45" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="60" y1="50" x2="60" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="75" y1="50" x2="75" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="90" y1="50" x2="90" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="105" y1="50" x2="105" y2="65" stroke="#90A4AE" strokeWidth="1.2" />

      {/* Right Wing */}
      <rect x="180" y="45" width="90" height="30" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="195" y1="50" x2="195" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="210" y1="50" x2="210" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="225" y1="50" x2="225" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="240" y1="50" x2="240" y2="65" stroke="#90A4AE" strokeWidth="1.2" />
      <line x1="255" y1="50" x2="255" y2="65" stroke="#90A4AE" strokeWidth="1.2" />

      {/* Ground Base Line */}
      <line x1="15" y1="78" x2="285" y2="78" stroke="#90A4AE" strokeWidth="1.5" />
      <line x1="10" y1="84" x2="290" y2="84" stroke="#90A4AE" strokeWidth="1.5" />
    </svg>
  );
}
