import React from 'react';

export default function RobotAvatar({ size = 40, className = "" }) {
  return (
    <div 
      className={`rounded-full flex items-center justify-center bg-white shadow-sm border border-[#E2D9CC] flex-shrink-0 ${className}`}
      style={{ width: size, height: size }}
    >
      <svg width={size * 0.75} height={size * 0.75} viewBox="0 0 40 40" fill="none">
        {/* Antennas */}
        <circle cx="20" cy="5" r="2.5" fill="#C59B27" />
        <line x1="20" y1="7" x2="20" y2="11" stroke="#8C6D46" strokeWidth="2" />
        <circle cx="8" cy="19" r="2" fill="#8C6D46" />
        <circle cx="32" cy="19" r="2" fill="#8C6D46" />

        {/* Head */}
        <rect x="9" y="11" width="22" height="18" rx="6" fill="#F8F6F0" stroke="#0F1E36" strokeWidth="2" />
        
        {/* Visor Area */}
        <rect x="12" y="15" width="16" height="8" rx="3.5" fill="#0F1E36" />
        
        {/* Eyes (Glowing Cyan) */}
        <circle cx="16" cy="19" r="2" fill="#38BDF8" />
        <circle cx="24" cy="19" r="2" fill="#38BDF8" />

        {/* Smile */}
        <path d="M17 24C18.5 25.5 21.5 25.5 23 24" stroke="#0F1E36" strokeWidth="1.5" strokeLinecap="round" />
        
        {/* Neck */}
        <rect x="17" y="29" width="6" height="3" fill="#C59B27" />
        
        {/* Body Top */}
        <path d="M12 32H28C31 32 32 34 32 36V38H8V36C8 34 9 32 12 32Z" fill="#0F1E36" />
      </svg>
    </div>
  );
}
