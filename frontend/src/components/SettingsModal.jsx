import React, { useState, useEffect } from 'react';
import { X, Key, Cpu, ShieldCheck, Check } from 'lucide-react';

export default function SettingsModal({ isOpen, onClose }) {
  const [apiKey, setApiKey] = useState('');
  const [hasKey, setHasKey] = useState(false);
  const [model, setModel] = useState('gemini-1.5-flash');
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetch('/api/settings')
        .then(res => res.json())
        .then(data => {
          setHasKey(data.has_gemini_key);
          if (data.gemini_model) setModel(data.gemini_model);
        })
        .catch(err => console.error(err));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          gemini_api_key: apiKey ? apiKey : undefined,
          gemini_model: model
        })
      });
      if (res.ok) {
        setSaveSuccess(true);
        setTimeout(() => setSaveSuccess(false), 2000);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-2xs animate-in fade-in duration-150">
      <div className="bg-white rounded-2xl max-w-md w-full border border-[#E2DAD0] shadow-2xl p-6 text-xs sm:text-sm">
        <div className="flex items-center justify-between pb-3 border-b border-[#F0EAE1]">
          <div className="flex items-center gap-2">
            <Key size={18} className="text-[#8B6B44]" />
            <h3 className="text-base font-bold text-[#0F1E36]">Gemini Model & API Settings</h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-[#F2ECE1] text-[#64748B]">
            <X size={18} />
          </button>
        </div>

        <div className="mt-4 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-[#1E293B] mb-1">
              Gemini API Key
            </label>
            <input
              type="password"
              placeholder={hasKey ? "Key configured on server (enter new to update)" : "Enter Gemini API key (e.g. AIzaSy...)"}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-[#D5C6AF] text-xs focus:outline-none focus:border-[#C5973A]"
            />
            <p className="text-[11px] text-[#64748B] mt-1 flex items-center gap-1">
              <ShieldCheck size={12} className="text-emerald-600" />
              <span>Key lives securely only on backend server (NFR-5).</span>
            </p>
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#1E293B] mb-1">
              Gemini Model Name (NFR-12)
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-[#D5C6AF] text-xs focus:outline-none focus:border-[#C5973A] bg-white"
            >
              <option value="gemini-1.5-flash">gemini-1.5-flash (Recommended: Fast & Grounded)</option>
              <option value="gemini-2.0-flash">gemini-2.0-flash</option>
              <option value="gemini-2.5-flash">gemini-2.5-flash</option>
              <option value="gemini-1.5-pro">gemini-1.5-pro</option>
            </select>
          </div>

          <div className="p-3 rounded-xl bg-[#FAF6EE] border border-[#E9DFCE] text-[11px] text-[#704F26] space-y-1">
            <div className="font-bold">SRS RAG Configuration:</div>
            <div>• Temperature: 0.1 (Strict grounding, no hallucination)</div>
            <div>• Top Chunks: 5 passages per query</div>
            <div>• Quote Verification: Enabled (AI-10)</div>
          </div>
        </div>

        <div className="mt-5 flex items-center justify-between pt-3 border-t border-[#F0EAE1]">
          {saveSuccess ? (
            <span className="text-emerald-700 font-semibold flex items-center gap-1 text-xs">
              <Check size={14} /> Saved!
            </span>
          ) : <span />}

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-3 py-1.5 rounded-xl border border-[#D5C6AF] text-[#64748B] hover:bg-[#FAF4EB] text-xs font-medium"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="px-4 py-1.5 rounded-xl bg-[#12223D] text-white text-xs font-semibold hover:bg-[#1E355B]"
            >
              {saving ? "Saving..." : "Save Settings"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
