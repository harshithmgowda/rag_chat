import React, { useState, useRef } from 'react';
import { FileText, UploadCloud, CheckCircle2, AlertCircle, Database, Layers, Sparkles, Plus } from 'lucide-react';
import { uploadPDF } from '../services/api';

export default function Sidebar({ documents, selectedDoc, onSelectDoc, onUploadSuccess, healthInfo }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null); // { type: 'success' | 'error', text: '' }
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      await processFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = async (e) => {
    if (e.target.files && e.target.files.length > 0) {
      await processFileUpload(e.target.files[0]);
    }
  };

  const processFileUpload = async (file) => {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setUploadStatus({ type: 'error', text: 'Please upload a valid .pdf file!' });
      return;
    }

    setIsUploading(true);
    setUploadStatus(null);

    try {
      const data = await uploadPDF(file);
      setUploadStatus({
        type: 'success',
        text: `Indexed ${data.total_pages} pages (${data.total_chunks} chunks)!`
      });
      if (onUploadSuccess) onUploadSuccess(data.filename);
    } catch (err) {
      setUploadStatus({
        type: 'error',
        text: err.message || 'Failed to upload PDF'
      });
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <aside className="sidebar">
      {/* Header / Logo */}
      <div className="sidebar-header">
        <div className="logo-badge">
          <Sparkles size={20} color="#fff" />
        </div>
        <div className="logo-text">
          <h1>PDF RAG Chatbot</h1>
          <p>Meta LLaMA 3.1 • ChromaDB</p>
        </div>
      </div>

      <div className="sidebar-content">
        {/* Upload Zone */}
        <div>
          <h3 style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Upload Any PDF
          </h3>
          <div
            className={`dropzone ${isDragging ? 'active' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".pdf"
              style={{ display: 'none' }}
            />
            <div className="dropzone-icon">
              {isUploading ? (
                <div className="animate-spin" style={{ width: 24, height: 24, border: '3px solid var(--accent-primary)', borderTopColor: 'transparent', borderRadius: '50%' }} />
              ) : (
                <UploadCloud size={24} />
              )}
            </div>
            <p style={{ fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              {isUploading ? 'Ingesting PDF...' : 'Drop ANY PDF here'}
            </p>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4 }}>
              or click to browse from disk
            </p>
          </div>

          {/* Upload Status Banner */}
          {uploadStatus && (
            <div
              style={{
                marginTop: 10,
                padding: '8px 12px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.8rem',
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                background: uploadStatus.type === 'success' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
                color: uploadStatus.type === 'success' ? 'var(--accent-emerald)' : 'var(--accent-rose)',
                border: `1px solid ${uploadStatus.type === 'success' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`
              }}
            >
              {uploadStatus.type === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
              <span>{uploadStatus.text}</span>
            </div>
          )}
        </div>

        {/* Documents List */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <h3 style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Indexed Documents ({documents.length})
            </h3>
            {selectedDoc && (
              <button
                onClick={() => onSelectDoc(null)}
                style={{ background: 'transparent', border: 'none', color: 'var(--accent-cyan)', fontSize: '0.75rem', cursor: 'pointer' }}
              >
                Search All
              </button>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, overflowY: 'auto' }}>
            {documents.length === 0 ? (
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic', padding: 8 }}>
                No PDFs uploaded yet. Drop a PDF above!
              </p>
            ) : (
              documents.map((doc) => (
                <div
                  key={doc}
                  className={`doc-card ${selectedDoc === doc ? 'selected' : ''}`}
                  onClick={() => onSelectDoc(doc === selectedDoc ? null : doc)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, overflow: 'hidden' }}>
                    <FileText size={18} color="var(--accent-primary)" style={{ flexShrink: 0 }} />
                    <span style={{ fontSize: '0.85rem', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {doc}
                    </span>
                  </div>
                  {selectedDoc === doc && (
                    <div style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-primary)' }} />
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* System Stats Footer */}
        <div style={{ padding: '12px 14px', background: 'var(--bg-glass-card)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)', display: 'flex', flexDirection: 'column', gap: 6 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <Database size={14} color="var(--accent-cyan)" />
              ChromaDB Storage:
            </span>
            <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
              {healthInfo?.total_chunks_indexed || 0} Chunks
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
