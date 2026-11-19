import React, { useState } from 'react';
import { Plus, Search, SlidersHorizontal, MoreVertical, BookOpen, Trash2, MessageSquare } from 'lucide-react';
import SKASCCrest from './SKASCCrest';
import BuildingGraphic from './BuildingGraphic';

export default function Sidebar({
  isOpen,
  onClose,
  sessions,
  currentSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
  onOpenHandbook
}) {
  const [searchTerm, setSearchTerm] = useState('');

  // Filter sessions by search term
  const filteredSessions = sessions.filter(s =>
    (s.title || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Group sessions into Today, Yesterday, Previous 7 Days, Older
  const now = new Date();
  const todaySessions = [];
  const yesterdaySessions = [];
  const pastWeekSessions = [];
  const olderSessions = [];

  filteredSessions.forEach(session => {
    const sDate = new Date(session.created_at || session.updated_at || Date.now());
    const diffDays = Math.floor((now - sDate) / (1000 * 60 * 60 * 24));
    if (diffDays === 0) {
      todaySessions.push(session);
    } else if (diffDays === 1) {
      yesterdaySessions.push(session);
    } else if (diffDays <= 7) {
      pastWeekSessions.push(session);
    } else {
      olderSessions.push(session);
    }
  });

  // Default sample history if empty to mirror mockup
  const displayToday = todaySessions.length > 0 ? todaySessions : [
    { id: 'sample-1', title: 'Minimum attendance percentage' },
    { id: 'sample-2', title: 'Exam rules and re-evaluation' }
  ];

  const displayYesterday = yesterdaySessions.length > 0 ? yesterdaySessions : [
    { id: 'sample-3', title: 'Dress code & campus conduct' }
  ];

  const displayPastWeek = pastWeekSessions.length > 0 ? pastWeekSessions : [
    { id: 'sample-4', title: 'Leave & scholarship policies' },
    { id: 'sample-5', title: 'Code of Conduct' }
  ];

  return (
    <aside 
      className={`fixed inset-y-0 left-0 z-40 w-72 bg-[#0B1728] text-white flex flex-col justify-between transition-transform duration-300 ease-in-out border-r border-[#19273D] ${
        isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      }`}
      style={{ minWidth: '18rem' }}
    >
      {/* Top Header / Brand */}
      <div className="p-4 border-b border-[#1A2A42]">
        <div className="flex items-center gap-3">
          <SKASCCrest size={46} />
          <div>
            <h1 className="text-[17px] font-bold text-white tracking-wide leading-tight">Polcy AI</h1>
            <p className="text-[11px] text-[#A6B7CC] font-medium tracking-tight">SKASC Policies Assistant</p>
          </div>
        </div>

        {/* New Chat Button */}
        <button
          onClick={onNewChat}
          className="mt-4 w-full flex items-center justify-center gap-2 py-2 px-4 rounded-full border border-[#D4A359] text-[#E5BF77] font-semibold text-sm hover:bg-[#D4A359]/15 transition-all shadow-sm active:scale-[0.98]"
        >
          <Plus size={16} className="text-[#D4A359]" />
          <span>New Chat</span>
        </button>

        {/* Search input with filter icon */}
        <div className="mt-3 relative flex items-center">
          <Search size={14} className="absolute left-3 text-[#7E8FA4]" />
          <input
            type="text"
            placeholder="Search chats..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-8 pr-8 py-1.5 rounded-lg bg-[#142236] border border-[#22354F] text-xs text-white placeholder-[#687B94] focus:outline-none focus:border-[#D4A359] transition-all"
          />
          <SlidersHorizontal size={14} className="absolute right-3 text-[#7E8FA4] hover:text-[#D4A359] cursor-pointer" />
        </div>
      </div>

      {/* History Sections */}
      <div className="flex-1 overflow-y-auto px-3 py-3 space-y-4 text-xs">
        {/* Today */}
        <div>
          <div className="px-2 pb-1 text-[11px] font-medium text-[#7E8FA4] flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#D4A359]"></span>
            <span>Today</span>
          </div>
          <div className="space-y-0.5">
            {displayToday.map((item) => (
              <div
                key={item.id}
                onClick={() => onSelectSession(item.id)}
                className={`group flex items-center justify-between px-2.5 py-2 rounded-lg cursor-pointer transition-colors ${
                  currentSessionId === item.id 
                    ? 'bg-[#182B45] text-white font-medium border-l-2 border-[#D4A359]' 
                    : 'text-[#B4C2D3] hover:bg-[#132236] hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  <MessageSquare size={13} className="text-[#899DB5] flex-shrink-0" />
                  <span className="truncate">{item.title}</span>
                </div>
                {onDeleteSession && !item.id.startsWith('sample-') && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteSession(item.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 text-[#7E8FA4]"
                    title="Delete Chat"
                  >
                    <Trash2 size={12} />
                  </button>
                )}
                {(item.id.startsWith('sample-') || !onDeleteSession) && (
                  <MoreVertical size={13} className="opacity-0 group-hover:opacity-60 text-[#7E8FA4]" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Yesterday */}
        <div>
          <div className="px-2 pb-1 text-[11px] font-medium text-[#7E8FA4]">
            Yesterday
          </div>
          <div className="space-y-0.5">
            {displayYesterday.map((item) => (
              <div
                key={item.id}
                onClick={() => onSelectSession(item.id)}
                className={`group flex items-center justify-between px-2.5 py-2 rounded-lg cursor-pointer transition-colors ${
                  currentSessionId === item.id 
                    ? 'bg-[#182B45] text-white font-medium border-l-2 border-[#D4A359]' 
                    : 'text-[#B4C2D3] hover:bg-[#132236] hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  <MessageSquare size={13} className="text-[#899DB5] flex-shrink-0" />
                  <span className="truncate">{item.title}</span>
                </div>
                <MoreVertical size={13} className="opacity-0 group-hover:opacity-60 text-[#7E8FA4]" />
              </div>
            ))}
          </div>
        </div>

        {/* Previous 7 Days */}
        <div>
          <div className="px-2 pb-1 text-[11px] font-medium text-[#7E8FA4]">
            Previous 7 Days
          </div>
          <div className="space-y-0.5">
            {displayPastWeek.map((item) => (
              <div
                key={item.id}
                onClick={() => onSelectSession(item.id)}
                className={`group flex items-center justify-between px-2.5 py-2 rounded-lg cursor-pointer transition-colors ${
                  currentSessionId === item.id 
                    ? 'bg-[#182B45] text-white font-medium border-l-2 border-[#D4A359]' 
                    : 'text-[#B4C2D3] hover:bg-[#132236] hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  <MessageSquare size={13} className="text-[#899DB5] flex-shrink-0" />
                  <span className="truncate">{item.title}</span>
                </div>
                <MoreVertical size={13} className="opacity-0 group-hover:opacity-60 text-[#7E8FA4]" />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Area with Handbook Link & Building Silhouette */}
      <div className="relative pt-2 pb-3 border-t border-[#1A2A42] overflow-hidden">
        <button
          onClick={onOpenHandbook}
          className="w-full flex items-center justify-between px-4 py-2.5 text-xs text-[#E5BF77] font-medium hover:bg-[#142338] transition-colors relative z-10"
        >
          <span className="flex items-center gap-2">
            <BookOpen size={14} className="text-[#D4A359]" />
            <span>SKASC Official Policy Handbook</span>
          </span>
          <span className="text-[#A6B7CC]">&gt;</span>
        </button>

        {/* College Building Sketch Watermark */}
        <div className="mt-1 px-4">
          <BuildingGraphic />
        </div>
      </div>
    </aside>
  );
}
