import React from 'react';
import { Users, FileSpreadsheet, Shirt, GraduationCap } from 'lucide-react';
import SKASCCrest from './SKASCCrest';

export default function WelcomeHero({ onSelectPrompt }) {
  const promptChips = [
    {
      id: 'attendance',
      icon: <Users size={16} className="text-[#8B6B44]" />,
      text: 'Minimum attendance percentage',
      query: 'What is the minimum attendance percentage?'
    },
    {
      id: 'exam',
      icon: <FileSpreadsheet size={16} className="text-[#8B6B44]" />,
      text: 'Exam malpractice & re-evaluation rules',
      query: 'What are the rules regarding exam malpractice and re-evaluation?'
    },
    {
      id: 'dress',
      icon: <Shirt size={16} className="text-[#8B6B44]" />,
      text: 'Dress code & campus conduct',
      query: 'What is the dress code and student code of conduct on campus?'
    },
    {
      id: 'scholarship',
      icon: <GraduationCap size={16} className="text-[#8B6B44]" />,
      text: 'Leave & scholarship policies',
      query: 'What are the scholarship and staff leave policies?'
    }
  ];

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-6">
      <div className="bg-white rounded-2xl border border-[#E7DFD1] p-6 sm:p-8 shadow-xs flex flex-col items-center text-center">
        {/* SKASC Crest Logo */}
        <div className="mb-3">
          <SKASCCrest size={76} />
        </div>

        {/* Welcome Title */}
        <h2 className="text-xl sm:text-2xl font-bold text-[#0F1E36] tracking-tight flex items-center gap-2">
          <span>Welcome to Polcy AI!</span>
          <span className="text-[#D4A359]">✨</span>
        </h2>

        {/* Subtitle */}
        <p className="mt-2 text-xs sm:text-sm text-[#475569] max-w-xl leading-relaxed">
          Your smart assistant to find official SKASC policies quickly and easily. Ask anything about academic, exam, or campus policies!
        </p>

        {/* Prompt Suggestion Cards (4 chips) */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 w-full">
          {promptChips.map((chip) => (
            <button
              key={chip.id}
              onClick={() => onSelectPrompt(chip.query)}
              className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl border border-[#DFD6C7] bg-[#FCFBF8] hover:bg-[#F8F2E6] hover:border-[#C5973A] transition-all text-left shadow-2xs group active:scale-[0.98]"
            >
              <div className="p-1.5 rounded-lg bg-white border border-[#EADFCF] group-hover:bg-[#F3EAD9] transition-colors flex-shrink-0">
                {chip.icon}
              </div>
              <span className="text-xs font-semibold text-[#1E293B] group-hover:text-[#0F1E36] leading-snug">
                {chip.text}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
