/**
 * API Service for communicating with FastAPI Backend
 */
const API_BASE_URL = 'http://localhost:8000/api';

export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Upload failed with status ${response.status}`);
  }

  return response.json();
}

export async function sendChatMessage(question, docName = null, topK = 3) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question,
      doc_name: docName,
      top_k: topK,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Chat request failed with status ${response.status}`);
  }

  return response.json();
}

export async function fetchDocuments() {
  const response = await fetch(`${API_BASE_URL}/documents`);
  if (!response.ok) throw new Error('Failed to fetch documents');
  return response.json();
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error('Backend health check failed');
  return response.json();
}
