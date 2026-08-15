import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, BookOpen, Sparkles, HelpCircle, FileCheck } from 'lucide-react';

export default function ChatArea({
  messages,
  onSendMessage,
  isLoading,
  selectedDoc,
  healthInfo
}) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const sampleSuggestions = [
    "What are the process states in an operating system?",
    "What is the security policy regarding leaked credentials?",
    "Why do LLMs hallucinate and how does RAG help?",
    "Explain virtual memory and paging in simple terms."
  ];

  return (
    <main className="main-chat">
      {/* Top Header */}
      <header className="chat-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div>
            <h2 style={{ fontSize: '1.05rem', fontWeight: 600 }}>
              {selectedDoc ? `Filtering: ${selectedDoc}` : 'Searching All Uploaded Documents'}
            </h2>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              LLM: Meta LLaMA 3.1 70B • Context-Grounded Search
            </p>
          </div>
        </div>

        <div className="header-status">
          <span className="status-dot" />
          <span>API Connected</span>
        </div>
      </header>

      {/* Messages Stream */}
      <div className="messages-container">
        {messages.length === 0 ? (
          <div style={{ margin: 'auto', textAlign: 'center', maxWidth: 500, padding: 20 }}>
            <div
              style={{
                width: 60,
                height: 60,
                margin: '0 auto 16px',
                borderRadius: 'var(--radius-lg)',
                background: 'var(--accent-gradient)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: 'var(--shadow-glow)'
              }}
            >
              <Sparkles size={32} color="#fff" />
            </div>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 8 }}>
              Ask Questions About Any PDF
            </h2>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Upload any PDF document using the sidebar, then ask questions. Answers are generated
              strictly from the text with exact page citations.
            </p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`message-bubble ${msg.sender === 'user' ? 'message-user' : 'message-bot'}`}
            >
              <div className={`message-avatar ${msg.sender === 'user' ? 'avatar-user' : 'avatar-bot'}`}>
                {msg.sender === 'user' ? <User size={18} /> : <Bot size={18} />}
              </div>

              <div className="message-body">
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <span style={{ fontSize: '0.8rem', fontWeight: 600, color: msg.sender === 'user' ? 'var(--accent-cyan)' : 'var(--accent-secondary)' }}>
                    {msg.sender === 'user' ? 'You' : 'PDF Assistant (LLaMA 3.1)'}
                  </span>
                </div>

                <div className="message-text">
                  {msg.text}
                </div>

                {/* Cited Sources & Page Numbers */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="sources-container">
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                      <BookOpen size={14} color="var(--accent-cyan)" /> Sources:
                    </span>
                    {msg.sources.map((src, i) => (
                      <span key={i} className="source-badge">
                        <FileCheck size={12} />
                        {src}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {/* Loading Bubble */}
        {isLoading && (
          <div className="message-bubble message-bot">
            <div className="message-avatar avatar-bot">
              <Bot size={18} />
            </div>
            <div className="message-body" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div className="animate-spin" style={{ width: 16, height: 16, border: '2px solid var(--accent-secondary)', borderTopColor: 'transparent', borderRadius: '50%' }} />
              <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
                Searching vector database & synthesizing answer with LLaMA 3.1...
              </span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Section */}
      <div className="chat-input-wrapper">
        {/* Suggestion Pills */}
        {messages.length === 0 && (
          <div className="suggestion-pills">
            {sampleSuggestions.map((s, idx) => (
              <button
                key={idx}
                className="pill-btn"
                onClick={() => onSendMessage(s)}
              >
                {s}
              </button>
            ))}
          </div>
        )}

        <form onSubmit={handleSubmit} className="input-box">
          <input
            type="text"
            placeholder={
              selectedDoc
                ? `Ask anything about ${selectedDoc}...`
                : "Ask anything about your uploaded documents..."
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" className="send-btn" disabled={!input.trim() || isLoading}>
            <Send size={16} />
            <span>Send</span>
          </button>
        </form>
      </div>
    </main>
  );
}
