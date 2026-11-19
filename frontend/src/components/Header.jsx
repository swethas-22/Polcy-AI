import React, { useState, useRef, useEffect } from 'react';
import { Menu, ChevronDown, RotateCcw, FileText, Settings, GraduationCap, Check } from 'lucide-react';

export default function Header({
  onToggleSidebar,
  selectedPolicy,
  onSelectPolicy,
  policies = [],
  onNewChat,
  activeDocument,
  onOpenDocumentModal,
  onOpenSettings
}) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="sticky top-0 z-30 bg-[#FBF9F4] border-b border-[#E8E2D6] px-4 py-2.5 flex items-center justify-between">
      {/* Left side: Hamburger & Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-1.5 rounded-lg hover:bg-[#EFE9DD] text-[#334155] transition-colors"
          title="Toggle Navigation Menu"
        >
          <Menu size={20} />
        </button>

        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <h1 className="text-base font-bold text-[#0F1E36] leading-none">Polcy AI</h1>
          </div>
          <p className="text-[11px] text-[#64748B] font-medium leading-none mt-1">SKASC Policies Assistant</p>
        </div>

        {/* Accreditation Pill Badge */}
        <div className="hidden lg:flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#FAF5EB] border border-[#D4A359]/70 text-[#7A5416] text-[11px] font-semibold tracking-tight shadow-2xs ml-3">
          <GraduationCap size={13} className="text-[#C5973A]" />
          <span>Autonomous | NAAC Accredited</span>
        </div>
      </div>

      {/* Right side: Policy Filter Dropdown, New Chat, Document Status, Settings */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Document Status Pill Button */}
        <button
          onClick={onOpenDocumentModal}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-full border border-[#DCD4C4] bg-white text-xs text-[#334155] hover:border-[#C5973A] transition-all shadow-2xs"
          title="Manage Uploaded Document (PDF, DOCX, TXT)"
        >
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <FileText size={13} className="text-[#64748B]" />
          <span className="hidden sm:inline font-medium text-[11.5px] max-w-[140px] truncate">
            {activeDocument ? activeDocument.filename : "SKASC Manual.docx"}
          </span>
        </button>

        {/* Policy Filter Dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-1.5 px-3 py-1 rounded-full border border-[#DCD4C4] bg-white text-xs font-medium text-[#1E293B] hover:border-[#C5973A] transition-colors shadow-2xs"
          >
            <span className="max-w-[130px] truncate">{selectedPolicy || "All Policies"}</span>
            <ChevronDown size={14} className="text-[#64748B]" />
          </button>

          {dropdownOpen && (
            <div className="absolute right-0 mt-1.5 w-64 max-h-80 overflow-y-auto bg-white rounded-xl shadow-lg border border-[#E2DAD0] py-1 text-xs z-50 animate-in fade-in zoom-in-95 duration-100">
              <div className="px-3 py-1.5 text-[11px] font-bold text-[#8A6B42] uppercase tracking-wider border-b border-[#F0EAE1]">
                Filter by Policy
              </div>
              <button
                onClick={() => {
                  onSelectPolicy("All Policies");
                  setDropdownOpen(false);
                }}
                className={`w-full text-left px-3 py-2 flex items-center justify-between hover:bg-[#FAF6EE] transition-colors ${
                  selectedPolicy === "All Policies" ? "bg-[#F7EEDB] font-bold text-[#7A5416]" : "text-[#334155]"
                }`}
              >
                <span>All Policies</span>
                {selectedPolicy === "All Policies" && <Check size={14} className="text-[#C5973A]" />}
              </button>
              {policies.map((p, idx) => {
                if (p === "All Policies") return null;
                const isSelected = selectedPolicy === p;
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      onSelectPolicy(p);
                      setDropdownOpen(false);
                    }}
                    className={`w-full text-left px-3 py-1.5 flex items-center justify-between hover:bg-[#FAF6EE] transition-colors ${
                      isSelected ? "bg-[#F7EEDB] font-bold text-[#7A5416]" : "text-[#334155]"
                    }`}
                  >
                    <span className="truncate pr-2">{p}</span>
                    {isSelected && <Check size={14} className="text-[#C5973A] flex-shrink-0" />}
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* New Chat Pill Button */}
        <button
          onClick={onNewChat}
          className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#12223D] text-white text-xs font-medium hover:bg-[#1C3256] transition-all shadow-sm active:scale-95"
        >
          <RotateCcw size={12} className="text-[#D4A359]" />
          <span>New Chat</span>
        </button>

        {/* Settings Button */}
        <button
          onClick={onOpenSettings}
          className="p-1.5 rounded-full hover:bg-[#EFE9DD] text-[#475569] transition-colors"
          title="Model & RAG Settings"
        >
          <Settings size={17} />
        </button>
      </div>
    </header>
  );
}
