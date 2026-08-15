import React, { useState, useRef } from 'react';
import { FileText, Upload, Check, AlertCircle, Database, Search, X, Layers } from 'lucide-react';
import { uploadPDF } from '../services/api';

export default function Sidebar({ documents, selectedDoc, onSelectDoc, onUploadSuccess, healthInfo }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
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
      setUploadStatus({ type: 'error', text: 'Only PDF documents are supported.' });
      return;
    }

    setIsUploading(true);
    setUploadStatus(null);

    try {
      const data = await uploadPDF(file);
      setUploadStatus({
        type: 'success',
        text: `Indexed ${data.total_pages} pages (${data.total_chunks} chunks)`
      });
      if (onUploadSuccess) onUploadSuccess(data.filename);
    } catch (err) {
      setUploadStatus({
        type: 'error',
        text: err.message || 'Upload failed'
      });
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const filteredDocs = documents.filter(doc => 
    doc.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <aside className="sidebar">
      {/* Top Header */}
      <div className="sidebar-top">
        <div className="brand-heading">
          <div className="brand-icon-box">
            <FileText size={16} />
          </div>
          <div>
            <div className="brand-title">RAG Document Studio</div>
            <div className="brand-subtitle">FastAPI • ChromaDB • LLaMA 3.1</div>
          </div>
        </div>
      </div>

      <div className="sidebar-body">
        {/* Upload Zone */}
        <div>
          <div className="section-label">
            <span>Import Document</span>
          </div>
          <div
            className={`clean-dropzone ${isDragging ? 'dragging' : ''}`}
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
            <div className="dropzone-upload-icon">
              {isUploading ? (
                <div style={{ width: 14, height: 14, border: '2px solid #a1a1aa', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
              ) : (
                <Upload size={16} />
              )}
            </div>
            <div>
              <div className="dropzone-text-main">
                {isUploading ? 'Indexing PDF...' : 'Upload PDF Document'}
              </div>
              <div className="dropzone-text-sub">Drag & drop or click to browse</div>
            </div>
          </div>

          {/* Status message */}
          {uploadStatus && (
            <div
              style={{
                marginTop: 8,
                padding: '6px 10px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.74rem',
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                background: uploadStatus.type === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(244, 63, 94, 0.1)',
                color: uploadStatus.type === 'success' ? 'var(--brand-emerald)' : 'var(--brand-rose)',
                border: `1px solid ${uploadStatus.type === 'success' ? 'rgba(16, 185, 129, 0.25)' : 'rgba(244, 63, 94, 0.25)'}`
              }}
            >
              {uploadStatus.type === 'success' ? <Check size={12} /> : <AlertCircle size={12} />}
              <span>{uploadStatus.text}</span>
            </div>
          )}
        </div>

        {/* Document List */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          <div className="section-label">
            <span>Documents ({documents.length})</span>
            {selectedDoc && (
              <button
                onClick={() => onSelectDoc(null)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', fontSize: '0.7rem', cursor: 'pointer' }}
              >
                Reset Filter
              </button>
            )}
          </div>

          {/* Search bar if multiple documents */}
          {documents.length > 2 && (
            <div style={{ display: 'flex', alignItems: 'center', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-sm)', padding: '5px 8px', marginBottom: 8 }}>
              <Search size={12} color="var(--text-muted)" style={{ marginRight: 6 }} />
              <input
                type="text"
                placeholder="Filter files..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ background: 'transparent', border: 'none', outline: 'none', color: 'var(--text-primary)', fontSize: '0.75rem', width: '100%' }}
              />
              {searchQuery && (
                <X size={12} color="var(--text-muted)" onClick={() => setSearchQuery('')} style={{ cursor: 'pointer' }} />
              )}
            </div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: 6, overflowY: 'auto', flex: 1 }}>
            {filteredDocs.length === 0 ? (
              <div style={{ padding: '12px 8px', fontSize: '0.76rem', color: 'var(--text-faint)', fontStyle: 'italic', textAlign: 'center' }}>
                {documents.length === 0 ? 'No documents indexed' : 'No matching files'}
              </div>
            ) : (
              filteredDocs.map((doc) => (
                <div
                  key={doc}
                  className={`doc-item ${selectedDoc === doc ? 'active' : ''}`}
                  onClick={() => onSelectDoc(doc === selectedDoc ? null : doc)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, overflow: 'hidden' }}>
                    <FileText size={14} color={selectedDoc === doc ? '#ffffff' : 'var(--text-muted)'} style={{ flexShrink: 0 }} />
                    <span className="doc-item-title">{doc}</span>
                  </div>
                  {selectedDoc === doc && (
                    <span style={{ fontSize: '0.68rem', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.1)', padding: '1px 5px', borderRadius: 3 }}>Active</span>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="sidebar-footer">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div className="status-pill">
            <span className="status-dot-green" />
            <span>Vector DB Connected</span>
          </div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
            {healthInfo?.total_chunks_indexed || 0} chunks
          </span>
        </div>
      </div>
    </aside>
  );
}
