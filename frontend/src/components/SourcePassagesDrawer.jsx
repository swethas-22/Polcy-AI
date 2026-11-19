import React from 'react';
import { X, BookOpen, FileText } from 'lucide-react';

export default function SourcePassagesDrawer({ isOpen, onClose, passages = [] }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-end bg-black/40 backdrop-blur-2xs animate-in fade-in duration-150">
      <div className="bg-[#FAF8F5] h-full w-full max-w-md shadow-2xl border-l border-[#E5DFD3] flex flex-col p-5 overflow-hidden">
        {/* Drawer Header */}
        <div className="flex items-center justify-between pb-3 border-b border-[#EADFCF]">
          <div className="flex items-center gap-2">
            <BookOpen size={18} className="text-[#8B6B44]" />
            <h3 className="font-bold text-[#0F1E36] text-sm">Retrieved Source Passages</h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-[#EFE7D8] text-[#64748B]">
            <X size={18} />
          </button>
        </div>

        <p className="text-[11px] text-[#64748B] mt-2 mb-3">
          These document passages were retrieved from the indexed document and fed into the Gemini API under the fixed system prompt.
        </p>

        {/* Passages List */}
        <div className="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
          {passages.map((p, idx) => (
            <div key={idx} className="bg-white rounded-xl border border-[#E5DFD3] p-3.5 shadow-2xs">
              <div className="flex items-center justify-between pb-1.5 mb-2 border-b border-[#F2ECE1]">
                <span className="font-bold text-[#83633C] text-[11px]">
                  {p.section || `Passage #${idx + 1}`}
                </span>
                <span className="px-2 py-0.5 rounded-md bg-[#FAF4EB] border border-[#E8DEC9] text-[#704F26] text-[10px] font-semibold">
                  Page {p.page || 1}
                </span>
              </div>
              <p className="text-[#334155] leading-relaxed text-[11.5px] whitespace-pre-wrap font-sans">
                {p.text}
              </p>
            </div>
          ))}

          {passages.length === 0 && (
            <div className="text-center py-10 text-gray-400">
              No passages retrieved for this response.
            </div>
          )}
        </div>

        <div className="pt-3 border-t border-[#EADFCF] flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-[#12223D] text-white text-xs font-semibold hover:bg-[#1E355B]"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
