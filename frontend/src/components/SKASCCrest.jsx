import React from 'react';

export default function SKASCCrest({ size = 48, className = "" }) {
  return (
    <svg 
      width={size} 
      height={size} 
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Laurel Wreath Left */}
      <path 
        d="M26 62C22 55 20 46 22 36C23 31 25 27 28 23C27 28 28 34 32 38C28 42 27 49 28 55C29 58 31 60 33 62" 
        stroke="#D4A359" 
        strokeWidth="3.2" 
        strokeLinecap="round" 
      />
      <circle cx="21" cy="42" r="3" fill="#D4A359" />
      <circle cx="24" cy="30" r="3" fill="#D4A359" />
      <circle cx="28" cy="22" r="3.2" fill="#D4A359" />
      <circle cx="22" cy="53" r="3" fill="#D4A359" />

      {/* Laurel Wreath Right */}
      <path 
        d="M74 62C78 55 80 46 78 36C77 31 75 27 72 23C73 28 72 34 68 38C72 42 73 49 72 55C71 58 69 60 67 62" 
        stroke="#D4A359" 
        strokeWidth="3.2" 
        strokeLinecap="round" 
      />
      <circle cx="79" cy="42" r="3" fill="#D4A359" />
      <circle cx="76" cy="30" r="3" fill="#D4A359" />
      <circle cx="72" cy="22" r="3.2" fill="#D4A359" />
      <circle cx="78" cy="53" r="3" fill="#D4A359" />

      {/* Central Shield / Crest Base */}
      <rect x="34" y="27" width="32" height="34" rx="4" fill="#0D1E38" stroke="#D4A359" strokeWidth="2.5" />
      
      {/* Open Book in Crest */}
      {/* Left Page */}
      <path d="M38 37C43 36 48 37 50 40V55C48 52 43 51 38 52V37Z" fill="#FAF5EB" stroke="#D4A359" strokeWidth="1.2" />
      {/* Right Page */}
      <path d="M62 37C57 36 52 37 50 40V55C52 52 57 51 62 52V37Z" fill="#FAF5EB" stroke="#D4A359" strokeWidth="1.2" />
      {/* Lines on Book */}
      <line x1="41" y1="42" x2="47" y2="42" stroke="#0D1E38" strokeWidth="1" strokeLinecap="round" />
      <line x1="41" y1="46" x2="47" y2="46" stroke="#0D1E38" strokeWidth="1" strokeLinecap="round" />
      <line x1="41" y1="50" x2="46" y2="50" stroke="#0D1E38" strokeWidth="1" strokeLinecap="round" />
      
      <line x1="53" y1="42" x2="59" y2="42" stroke="#0D1E38" strokeWidth="1" strokeLinecap="round" />
      <line x1="53" y1="46" x2="59" y2="46" stroke="#0D1E38" strokeWidth="1" strokeLinecap="round" />
      <line x1="53" y1="50" x2="58" y2="50" stroke="#0D1E38" strokeWidth="1" strokeLinecap="round" />

      {/* Banner / Ribbon */}
      <path d="M22 66L30 63H70L78 66L74 74H26L22 66Z" fill="#A87932" stroke="#5E3F11" strokeWidth="1.2" />
      <text 
        x="50" 
        y="71.5" 
        textAnchor="middle" 
        fill="#FFFFFF" 
        fontSize="8.5" 
        fontWeight="800" 
        letterSpacing="0.8" 
        fontFamily="sans-serif"
      >
        SKASC
      </text>
    </svg>
  );
}
