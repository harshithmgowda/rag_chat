import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Copy, Check, Trash2, FileText, Bookmark, CornerDownLeft } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function ChatArea({
  messages,
  onSendMessage,
  isLoading,
  selectedDoc,
  onClearChat
}) {
  const [input, setInput] = useState('');
  const [copiedIndex, setCopiedIndex] = useState(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const copyToClipboard = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleTextareaInput = (e) => {
    setInput(e.target.value);
    // Auto-adjust height
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 120)}px`;
  };

  const suggestedPrompts = [
    { title: "Operating System States", desc: "List and explain the 5 process execution states." },
    { title: "API Security Policies", desc: "What is the policy for handling leaked credentials?" },
    { title: "Virtual Memory & Paging", desc: "How does the OS translate virtual pages to physical frames?" },
    { title: "Document Summary", desc: "Provide an executive summary of the uploaded document." }
  ];

  return (
    <main className="main-viewport">
      {/* Top Navbar */}
      <header className="top-navbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div className="active-filter-badge">
            <FileText size={12} />
            <span>{selectedDoc ? selectedDoc : 'All Indexed Documents'}</span>
          </div>
          <span style={{ fontSize: '0.74rem', color: 'var(--text-faint)' }}>•</span>
          <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Meta LLaMA 3.1 70B</span>
        </div>

        {messages.length > 0 && (
          <button onClick={onClearChat} className="clear-btn" title="Clear chat history">
            <Trash2 size={13} />
            <span>Clear</span>
          </button>
        )}
      </header>

      {/* Message Stream */}
      <div className="chat-scroll-area">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div style={{ width: 36, height: 36, borderRadius: 'var(--radius-sm)', background: '#1c1c22', border: '1px solid var(--border-medium)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px', color: '#ffffff' }}>
              <FileText size={18} />
            </div>
            <h1 className="empty-state-title">Ask anything about your documents</h1>
            <p className="empty-state-desc">
              Upload any PDF document on the left. The system indexes text chunks and provides
              strictly grounded answers with exact page citations.
            </p>

            <div className="prompt-grid">
              {suggestedPrompts.map((p, idx) => (
                <div
                  key={idx}
                  className="prompt-card"
                  onClick={() => onSendMessage(p.desc)}
                >
                  <div className="prompt-card-title">{p.title}</div>
                  <div className="prompt-card-sub">{p.desc}</div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className="message-wrapper">
              {msg.sender === 'user' ? (
                <div className="user-row">
                  <div className="user-bubble">
                    {msg.text}
                  </div>
                </div>
              ) : (
                <div className="bot-row">
                  <div className="bot-header">
                    <span>ASSISTANT</span>
                    <button
                      onClick={() => copyToClipboard(msg.text, index)}
                      style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 4, fontSize: '0.72rem' }}
                    >
                      {copiedIndex === index ? <Check size={12} color="var(--brand-emerald)" /> : <Copy size={12} />}
                      <span>{copiedIndex === index ? 'Copied' : 'Copy'}</span>
                    </button>
                  </div>

                  <div className="bot-content">
                    <ReactMarkdown>{msg.text}</ReactMarkdown>

                    {/* Sources / Citations */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="citations-box">
                        <div className="citations-header">
                          <Bookmark size={11} />
                          <span>Cited Sources</span>
                        </div>
                        <div className="citation-chips">
                          {msg.sources.map((src, i) => (
                            <span key={i} className="citation-chip">
                              {src}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))
        )}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="message-wrapper">
            <div className="bot-row">
              <div className="bot-header">
                <span>ASSISTANT</span>
              </div>
              <div className="bot-content" style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                <div style={{ width: 12, height: 12, border: '2px solid var(--text-muted)', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
                <span>Searching vector store & generating response...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Dock */}
      <div className="input-dock">
        <div className="input-container">
          <textarea
            ref={textareaRef}
            rows={1}
            className="chat-input"
            placeholder={selectedDoc ? `Ask about ${selectedDoc}...` : "Ask any question about your documents..."}
            value={input}
            onChange={handleTextareaInput}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            className="submit-btn"
            disabled={!input.trim() || isLoading}
            title="Send message"
          >
            <ArrowUp size={14} />
          </button>
        </div>
        <div className="input-hint">
          <span>Press <strong>Enter</strong> to send • <strong>Shift + Enter</strong> for new line</span>
        </div>
      </div>
    </main>
  );
}
