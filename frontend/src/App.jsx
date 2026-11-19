import React, { useState, useEffect, useRef } from 'react';
import { Send, Paperclip } from 'lucide-react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import WelcomeHero from './components/WelcomeHero';
import ChatMessageItem from './components/ChatMessageItem';
import DocumentModal from './components/DocumentModal';
import SettingsModal from './components/SettingsModal';
import HandbookModal from './components/HandbookModal';
import SourcePassagesDrawer from './components/SourcePassagesDrawer';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputQuestion, setInputQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeDocument, setActiveDocument] = useState(null);
  const [selectedPolicy, setSelectedPolicy] = useState('All Policies');
  const [policies, setPolicies] = useState(['All Policies']);

  // Modals state
  const [docModalOpen, setDocModalOpen] = useState(false);
  const [settingsModalOpen, setSettingsModalOpen] = useState(false);
  const [handbookModalOpen, setHandbookModalOpen] = useState(false);
  const [passagesDrawerOpen, setPassagesDrawerOpen] = useState(false);
  const [currentPassages, setCurrentPassages] = useState([]);

  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Load initial session and policies on mount
  useEffect(() => {
    fetchSessions();
    fetchPolicies();
  }, []);

  const fetchPolicies = async () => {
    try {
      const res = await fetch('/api/policies');
      if (res.ok) {
        const data = await res.json();
        if (data.policies && data.policies.length > 0) {
          setPolicies(data.policies);
        }
      }
    } catch (err) {
      console.error("Error fetching policies:", err);
    }
  };

  const fetchSessions = async () => {
    try {
      const res = await fetch('/api/sessions');
      if (res.ok) {
        const data = await res.json();
        setSessions(data);
        if (data.length > 0) {
          selectSession(data[0].id);
        } else {
          startNewChat();
        }
      } else {
        startNewChat();
      }
    } catch (err) {
      console.error("Error fetching sessions:", err);
      startNewChat();
    }
  };

  const selectSession = async (sessionId) => {
    setCurrentSessionId(sessionId);
    try {
      const res = await fetch(`/api/sessions/${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || []);
        if (data.active_document) {
          setActiveDocument(data.active_document);
        }
      }
    } catch (err) {
      console.error("Error loading session:", err);
    }
  };

  const startNewChat = async () => {
    try {
      const res = await fetch('/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ preload_skasc: true })
      });
      if (res.ok) {
        const data = await res.json();
        setCurrentSessionId(data.session_id);
        setMessages([]);
        if (data.active_document) {
          setActiveDocument(data.active_document);
        }
        setSessions(prev => [
          { id: data.session_id, title: data.title, created_at: data.created_at },
          ...prev
        ]);
      }
    } catch (err) {
      console.error("Error creating new chat:", err);
    }
  };

  const deleteSession = async (sessionId) => {
    try {
      await fetch(`/api/sessions/${sessionId}`, { method: 'DELETE' });
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      if (currentSessionId === sessionId) {
        startNewChat();
      }
    } catch (err) {
      console.error("Error deleting session:", err);
    }
  };

  const handleSendMessage = async (customQuery = null) => {
    const q = (customQuery || inputQuestion).trim();
    if (!q || loading) return;

    // Append optimistic user message
    const tempUserMsg = {
      id: 'temp-' + Date.now(),
      role: 'user',
      content: q,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);
    setInputQuestion('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: currentSessionId,
          question: q,
          policy_filter: selectedPolicy
        })
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to get answer');
      }

      // Add assistant response
      const assistantMsg = {
        id: data.assistant_message_id || 'bot-' + Date.now(),
        role: 'assistant',
        content: data.answer,
        reply_type: data.reply_type,
        policy_tags: data.policy_tags || [],
        source_passages: data.source_passages || [],
        created_at: data.timestamp || new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMsg]);

      // Update session title in history if first message
      if (messages.length === 0) {
        setSessions(prev => prev.map(s => s.id === currentSessionId ? { ...s, title: q.slice(0, 35) } : s));
      }
    } catch (err) {
      const errorMsg = {
        id: 'err-' + Date.now(),
        role: 'assistant',
        content: `Error: ${err.message || 'Unable to connect to policy assistant.'}`,
        reply_type: 'error',
        policy_tags: [],
        source_passages: [],
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handlePreloadSKASC = async () => {
    const res = await fetch('/api/documents/preload_skasc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: currentSessionId })
    });
    const data = await res.json();
    if (res.ok) {
      setActiveDocument(data.document);
      fetchPolicies();
    } else {
      throw new Error(data.error || 'Failed to preload');
    }
  };

  const handleDeleteDocument = async () => {
    if (!activeDocument) return;
    try {
      await fetch(`/api/documents/${activeDocument.id}`, { method: 'DELETE' });
      setActiveDocument(null);
      setDocModalOpen(false);
    } catch (err) {
      console.error(err);
    }
  };

  const openPassagesViewer = (passages) => {
    setCurrentPassages(passages);
    setPassagesDrawerOpen(true);
  };

  return (
    <div className="flex h-screen bg-[#FAF7F2] text-[#1E293B] overflow-hidden">
      {/* Sidebar Navigation */}
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={(id) => {
          selectSession(id);
          setSidebarOpen(false);
        }}
        onNewChat={() => {
          startNewChat();
          setSidebarOpen(false);
        }}
        onDeleteSession={deleteSession}
        onOpenHandbook={() => setHandbookModalOpen(true)}
      />

      {/* Main Chat View */}
      <div className="flex-1 flex flex-col h-full overflow-hidden md:ml-72 transition-all">
        {/* Top Header */}
        <Header
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          selectedPolicy={selectedPolicy}
          onSelectPolicy={setSelectedPolicy}
          policies={policies}
          onNewChat={startNewChat}
          activeDocument={activeDocument}
          onOpenDocumentModal={() => setDocModalOpen(true)}
          onOpenSettings={() => setSettingsModalOpen(true)}
        />

        {/* Chat Thread Messages Area */}
        <main className="flex-1 overflow-y-auto px-4 py-4 max-w-4xl w-full mx-auto">
          {/* Welcome Card if chat is clean or only 0/1 message */}
          {messages.length === 0 && (
            <WelcomeHero onSelectPrompt={(prompt) => handleSendMessage(prompt)} />
          )}

          {/* Messages */}
          {messages.map((msg, index) => (
            <ChatMessageItem
              key={msg.id || index}
              message={msg}
              onOpenPassages={openPassagesViewer}
            />
          ))}

          {/* Searching Status Indicator (UI-4) */}
          {loading && (
            <div className="flex items-center gap-2 mb-4 text-xs font-semibold text-[#83633C] pl-2 animate-pulse">
              <span className="flex gap-1">
                <span className="w-2 h-2 rounded-full bg-[#83633C] dot-1"></span>
                <span className="w-2 h-2 rounded-full bg-[#83633C] dot-2"></span>
                <span className="w-2 h-2 rounded-full bg-[#83633C] dot-3"></span>
              </span>
              <span>Searching SKASC policies...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </main>

        {/* Chat Input Bar at Bottom */}
        <footer className="p-4 border-t border-[#EAE3D5] bg-[#FAF7F2] max-w-4xl w-full mx-auto">
          <div className="bg-white rounded-2xl border border-[#DCD3C3] shadow-xs px-3.5 py-2.5 flex items-center gap-2.5 transition-all focus-within:border-[#C5973A] focus-within:ring-1 focus-within:ring-[#C5973A]/40">
            {/* Attachment Button for Document Management */}
            <button
              onClick={() => setDocModalOpen(true)}
              className="p-1.5 rounded-lg text-[#64748B] hover:text-[#0F1E36] hover:bg-[#F6EFE3] transition-colors"
              title="Upload / Manage Policy Document (PDF, DOCX, TXT)"
            >
              <Paperclip size={18} />
            </button>

            {/* Input Field */}
            <textarea
              rows={1}
              value={inputQuestion}
              onChange={(e) => setInputQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about SKASC academic, exam, or campus policies..."
              className="flex-1 bg-transparent border-none outline-none text-xs sm:text-sm text-[#0F1E36] placeholder-[#8C9AA8] resize-none max-h-32 leading-relaxed"
            />

            {/* Send Button */}
            <button
              onClick={() => handleSendMessage()}
              disabled={!inputQuestion.trim() || loading}
              className="flex items-center gap-1.5 px-4 py-2 rounded-full bg-[#12223D] text-white text-xs font-semibold hover:bg-[#1C3256] disabled:opacity-40 disabled:hover:bg-[#12223D] transition-all active:scale-95 shadow-2xs"
            >
              <Send size={13} className="text-[#D4A359]" />
              <span>Send</span>
            </button>
          </div>

          <p className="text-center text-[11px] text-[#8C9AA8] mt-2 font-medium">
            Press Enter to send • Shift + Enter for newline
          </p>
        </footer>
      </div>

      {/* Modals & Drawers */}
      <DocumentModal
        isOpen={docModalOpen}
        onClose={() => setDocModalOpen(false)}
        activeDocument={activeDocument}
        onUploadSuccess={(doc) => {
          setActiveDocument(doc);
          fetchPolicies();
        }}
        onDeleteDocument={handleDeleteDocument}
        onPreloadSKASC={handlePreloadSKASC}
      />

      <SettingsModal
        isOpen={settingsModalOpen}
        onClose={() => setSettingsModalOpen(false)}
      />

      <HandbookModal
        isOpen={handbookModalOpen}
        onClose={() => setHandbookModalOpen(false)}
      />

      <SourcePassagesDrawer
        isOpen={passagesDrawerOpen}
        onClose={() => setPassagesDrawerOpen(false)}
        passages={currentPassages}
      />
    </div>
  );
}
