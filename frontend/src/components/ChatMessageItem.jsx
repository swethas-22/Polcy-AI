import React, { useState } from 'react';
import { Copy, Check, CheckCheck, User, ExternalLink, ShieldCheck } from 'lucide-react';
import RobotAvatar from './RobotAvatar';

export default function ChatMessageItem({ message, onOpenPassages }) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Format timestamp (e.g., 10:24 AM)
  const formatTime = (isoString) => {
    try {
      const d = isoString ? new Date(isoString) : new Date();
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return "10:25 AM";
    }
  };

  if (isUser) {
    return (
      <div className="flex justify-end items-end gap-2 mb-4">
        <div className="flex flex-col items-end max-w-[85%] sm:max-w-[70%]">
          <div className="bg-[#12223D] text-white px-4 py-2.5 rounded-2xl rounded-br-xs text-xs sm:text-sm leading-relaxed shadow-xs">
            {message.content}
          </div>
          <div className="flex items-center gap-1 mt-1 text-[11px] text-[#8C9AA8] font-medium pr-1">
            <span>{formatTime(message.created_at)}</span>
            <CheckCheck size={14} className="text-[#38BDF8]" />
          </div>
        </div>

        {/* User Avatar */}
        <div className="w-8 h-8 rounded-full bg-[#12223D] flex items-center justify-center text-white flex-shrink-0 shadow-2xs">
          <User size={16} />
        </div>
      </div>
    );
  }

  // Assistant Message
  const policyTags = message.policy_tags || [];
  const sourcePassages = message.source_passages || [];

  return (
    <div className="flex justify-start items-start gap-2.5 mb-6">
      {/* Robot Avatar */}
      <RobotAvatar size={38} className="mt-1" />

      {/* Assistant Card */}
      <div className="flex flex-col items-start max-w-[90%] sm:max-w-[82%]">
        <div className="bg-white rounded-2xl border border-[#E7DFD1] p-4 sm:p-5 text-xs sm:text-sm text-[#1E293B] shadow-xs w-full">
          {/* Policy Badges at Top (Matching Mockup: Attendance Policy, Section 3.2, etc.) */}
          {policyTags.length > 0 && (
            <div className="flex flex-wrap items-center gap-1.5 mb-3">
              {policyTags.slice(0, 3).map((tag, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-0.5 rounded-full bg-[#83633C] text-white text-[10.5px] font-semibold tracking-tight shadow-2xs"
                >
                  {tag}
                </span>
              ))}
              {sourcePassages.length > 0 && (
                <span className="px-2.5 py-0.5 rounded-full bg-[#9E7A4E] text-white text-[10.5px] font-semibold tracking-tight shadow-2xs">
                  {sourcePassages[0].section ? `Section ${sourcePassages[0].section.split(' ')[0]}` : `Page ${sourcePassages[0].page}`}
                </span>
              )}
            </div>
          )}

          {/* Formatted Content */}
          <div className="prose prose-sm max-w-none space-y-1.5 text-[#1E293B] leading-relaxed">
            {message.content.split('\n').map((line, i) => {
              const trimmed = line.trim();
              if (!trimmed) return <div key={i} className="h-1" />;
              
              if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
                return (
                  <div key={i} className="flex items-start gap-2 pl-1 my-0.5">
                    <span className="text-[#83633C] font-bold text-sm leading-none mt-0.5">•</span>
                    <span className="flex-1 text-xs sm:text-sm">{trimmed.replace(/^[•\-]\s*/, '')}</span>
                  </div>
                );
              }

              if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
                return (
                  <p key={i} className="font-bold text-[#0F1E36] text-xs sm:text-sm mt-2">
                    {trimmed.replace(/\*\*/g, '')}
                  </p>
                );
              }

              return (
                <p key={i} className="text-xs sm:text-sm">
                  {trimmed}
                </p>
              );
            })}
          </div>

          {/* Verification Badge & Source Passages Action */}
          <div className="mt-4 pt-3 border-t border-[#F2ECE1] flex flex-wrap items-center justify-between gap-2 text-[11px] text-[#64748B]">
            <div className="flex items-center gap-1.5 text-[#73542E] font-medium">
              <ShieldCheck size={14} className="text-[#9E7A4E]" />
              <span>Verify with Administrative Office</span>
            </div>

            <div className="flex items-center gap-3">
              {sourcePassages.length > 0 && (
                <button
                  onClick={() => onOpenPassages(sourcePassages)}
                  className="flex items-center gap-1 text-[#83633C] hover:text-[#0F1E36] font-semibold transition-colors underline cursor-pointer"
                >
                  <ExternalLink size={12} />
                  <span>View Source Passages ({sourcePassages.length})</span>
                </button>
              )}

              {/* Copy Button (FR-26) */}
              <button
                onClick={handleCopy}
                className="flex items-center gap-1 p-1 hover:bg-[#FAF6EE] rounded text-[#64748B] hover:text-[#0F1E36] transition-colors"
                title="Copy Answer"
              >
                {copied ? <Check size={13} className="text-emerald-600" /> : <Copy size={13} />}
                <span>{copied ? "Copied" : "Copy"}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Timestamp */}
        <div className="mt-1 text-[11px] text-[#8C9AA8] font-medium pl-2">
          {formatTime(message.created_at)}
        </div>
      </div>
    </div>
  );
}
