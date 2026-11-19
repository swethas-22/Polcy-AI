import React, { useState, useRef } from 'react';
import { X, UploadCloud, FileText, CheckCircle2, AlertCircle, RefreshCw, Trash2, ShieldAlert } from 'lucide-react';

export default function DocumentModal({
  isOpen,
  onClose,
  activeDocument,
  onUploadSuccess,
  onDeleteDocument,
  onPreloadSKASC
}) {
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const fileInputRef = useRef(null);

  if (!isOpen) return null;

  const handleFileUpload = async (file) => {
    setErrorMsg('');
    setSuccessMsg('');

    if (!file) return;

    // Check extension (FR-3)
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx', 'txt'].includes(ext)) {
      setErrorMsg(`Unsupported file type (.${ext}). Only PDF, DOCX, and TXT files are accepted.`);
      return;
    }

    // Check size (FR-4: 20MB limit)
    const maxBytes = 20 * 1024 * 1024;
    if (file.size > maxBytes) {
      setErrorMsg(`File size (${(file.size / (1024 * 1024)).toFixed(1)} MB) exceeds the 20 MB limit.`);
      return;
    }

    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch('/api/documents', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to upload document');
      }

      setSuccessMsg(`Document "${file.name}" uploaded and indexed successfully!`);
      if (onUploadSuccess) onUploadSuccess(data.document);
    } catch (err) {
      setErrorMsg(err.message || 'Error uploading document');
    } finally {
      setUploading(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handlePreload = async () => {
    setErrorMsg('');
    setSuccessMsg('');
    setUploading(true);
    try {
      await onPreloadSKASC();
      setSuccessMsg("Preloaded Sri Krishna Arts and Science College Policy Manual (.docx) successfully!");
    } catch (err) {
      setErrorMsg(err.message || 'Failed to preload policy manual');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-2xs animate-in fade-in duration-150">
      <div className="bg-white rounded-2xl max-w-lg w-full border border-[#E2DAD0] shadow-2xl p-6 text-xs sm:text-sm">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-[#F0EAE1]">
          <div>
            <h3 className="text-base font-bold text-[#0F1E36]">Document Knowledge Base</h3>
            <p className="text-xs text-[#64748B] mt-0.5">Manage the source document used for RAG grounding</p>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-[#F2ECE1] text-[#64748B]">
            <X size={18} />
          </button>
        </div>

        {/* Current Active Document */}
        <div className="mt-4 p-3.5 rounded-xl bg-[#FAF6EE] border border-[#E9DFCE] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-white border border-[#DDD3C2] text-[#83633C]">
              <FileText size={20} />
            </div>
            <div>
              <div className="font-bold text-[#0F1E36] text-xs sm:text-sm truncate max-w-[240px]">
                {activeDocument ? activeDocument.filename : "SKASC_Policy_Manual_2026_2027.docx"}
              </div>
              <div className="text-[11px] text-[#718096] flex items-center gap-2 mt-0.5">
                <span className="flex items-center gap-1 text-emerald-700 font-semibold">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                  Ready for RAG
                </span>
                <span>•</span>
                <span>{activeDocument ? `${activeDocument.chunks_count || 229} Chunks Indexed` : "229 Chunks Indexed"}</span>
              </div>
            </div>
          </div>

          {activeDocument && (
            <button
              onClick={onDeleteDocument}
              className="p-1.5 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Delete Document"
            >
              <Trash2 size={16} />
            </button>
          )}
        </div>

        {/* Messages */}
        {errorMsg && (
          <div className="mt-3 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
            <AlertCircle size={15} className="flex-shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {successMsg && (
          <div className="mt-3 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2">
            <CheckCircle2 size={15} className="flex-shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Drag & Drop Upload Zone (FR-2, FR-3, FR-4) */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={onDrop}
          onClick={() => fileInputRef.current && fileInputRef.current.click()}
          className={`mt-4 border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors ${
            dragOver ? 'border-[#C5973A] bg-[#FAF5EB]' : 'border-[#D9CFBF] bg-[#FCFBF8] hover:bg-[#F9F4EB]'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => handleFileUpload(e.target.files[0])}
            accept=".pdf,.docx,.txt"
            className="hidden"
          />

          <UploadCloud size={32} className="mx-auto text-[#83633C] mb-2" />
          <p className="font-semibold text-[#0F1E36] text-xs sm:text-sm">
            Click to upload or drag & drop document
          </p>
          <p className="text-[11px] text-[#64748B] mt-1">
            Supports PDF, DOCX, or TXT (Max size: 20 MB)
          </p>
          {uploading && (
            <div className="mt-3 flex items-center justify-center gap-2 text-xs text-[#83633C] font-semibold">
              <RefreshCw size={14} className="animate-spin" />
              <span>Parsing and indexing document chunks...</span>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="mt-5 flex items-center justify-between gap-3 pt-3 border-t border-[#F0EAE1]">
          <button
            onClick={handlePreload}
            disabled={uploading}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl border border-[#D5C6AF] text-[#704F26] font-semibold hover:bg-[#FAF4EB] transition-colors text-xs disabled:opacity-50"
          >
            <RefreshCw size={13} className={uploading ? "animate-spin" : ""} />
            <span>Reset to SKASC Policy Manual (Word DOCX)</span>
          </button>

          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-[#12223D] text-white font-semibold hover:bg-[#1E355B] transition-colors text-xs"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
