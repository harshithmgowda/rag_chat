import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import { fetchDocuments, sendChatMessage, checkHealth } from './services/api';

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [healthInfo, setHealthInfo] = useState(null);

  // Load initial documents and system health
  const refreshData = async () => {
    try {
      const docData = await fetchDocuments();
      setDocuments(docData.documents || []);

      const health = await checkHealth();
      setHealthInfo(health);
    } catch (err) {
      console.warn("Backend not yet running or still initializing:", err);
    }
  };

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 10000); // Poll health & docs every 10s
    return () => clearInterval(interval);
  }, []);

  const handleUploadSuccess = (newDocName) => {
    refreshData();
    setSelectedDoc(newDocName);
    setMessages((prev) => [
      ...prev,
      {
        sender: 'bot',
        text: `📄 Successfully uploaded and indexed "${newDocName}" into ChromaDB! You can now ask any question about it.`,
        sources: []
      }
    ]);
  };

  const handleSendMessage = async (question) => {
    // Append user message immediately
    setMessages((prev) => [
      ...prev,
      { sender: 'user', text: question }
    ]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(question, selectedDoc, 3);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: response.answer,
          sources: response.sources
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: `❌ Error communicating with backend: ${err.message}`,
          sources: []
        }
      ]);
    } finally {
      setIsLoading(false);
      refreshData();
    }
  };

  return (
    <div className="app-container">
      <Sidebar
        documents={documents}
        selectedDoc={selectedDoc}
        onSelectDoc={setSelectedDoc}
        onUploadSuccess={handleUploadSuccess}
        healthInfo={healthInfo}
      />
      <ChatArea
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        selectedDoc={selectedDoc}
        healthInfo={healthInfo}
      />
    </div>
  );
}
