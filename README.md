# 🚀 PDF RAG Chatbot 

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-orange.svg)](https://www.trychroma.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-grade, full-stack **Retrieval-Augmented Generation (RAG)** web application and CLI chatbot that lets you upload **ANY multi-page PDF**, indexes it into a local vector database, and answers user questions with **100% factual grounding and exact page citations** using **Meta LLaMA 3.1 70B** on **NVIDIA NIM API** and **ChromaDB**.

---

## 🧠 What is RAG? (ELI10 - Explain Like I'm 10)

Traditional AI models answer questions from memory like taking a **closed-book exam**. If they don't know something about your private documents, they might guess or hallucinate.

**RAG (Retrieval-Augmented Generation)** is like an **open-book exam**:
1. 📄 **Upload:** You give the system your private PDF.
2. 🧩 **Chunking:** The system cuts the document into bite-sized paragraphs.
3. 🔢 **Embeddings:** Each paragraph is converted into 384 numbers (vectors) representing its meaning.
4. 🗄️ **Vector Database:** The vectors are stored in **ChromaDB**.
5. 🔍 **Retrieval:** When you ask a question, ChromaDB instantly retrieves the top 3 most relevant paragraphs.
6. 🤖 **LLM Generation:** The AI (LLaMA 3.1) reads *only those 3 paragraphs* and writes a strictly accurate answer with page citations.

---

## 🏗️ Architecture Diagram

```text
========================================================================
1. INGESTION PIPELINE (When ANY PDF is uploaded)
========================================================================
📄 Uploaded PDF (Any document)
   │
   ▼  PyMuPDF (fitz)
📝 Clean Text + Page Numbers
   │
   ▼  Sliding-Window Chunking (chunk_size=350, overlap=50)
🧩 Structured Chunks
   │
   ▼  SentenceTransformer (all-MiniLM-L6-v2)
🔢 384-dimensional Embeddings
   │
   ▼  ChromaDB.upsert(ids, documents, embeddings, metadatas)
🗄️ Persistent Vector Database (data/chroma/)


========================================================================
2. QUERY PIPELINE (When User asks a question)
========================================================================
❓ User Question ("What are the process states?")
   │
   ▼  SentenceTransformer.encode()
🔢 Question Vector
   │
   ▼  ChromaDB.query(n_results=3, where={"doc_name": doc})
📄 Top-3 Relevant Chunks + Page Numbers
   │
   ▼  Prompt Construction (Strict Anti-Hallucination Persona)
📜 Context-Augmented Prompt
   │
   ▼  OpenAI SDK -> NVIDIA NIM API
🤖 Meta LLaMA 3.1 70B
   │
   ▼
🎯 Grounded Answer + Source Citations ("Page 2 (OperatingSystems.pdf)")
```

---

## 🛠️ Technology Stack

### Backend
* **Python 3.10+**
* **FastAPI:** High-performance async REST API framework.
* **PyMuPDF (`pymupdf`):** Ultra-fast PDF page-by-page text parsing.
* **Sentence-Transformers (`all-MiniLM-L6-v2`):** Local 384-dimensional dense semantic embeddings.
* **ChromaDB:** Persistent on-disk vector database.
* **Meta LLaMA 3.1 70B (NVIDIA NIM / OpenAI-compatible API):** LLM generation engine.
* **Pydantic:** Strict schema request/response validation.
* **Pytest:** Comprehensive unit & integration testing.

### Frontend
* **React + Vite:** Ultra-fast, modular web framework.
* **Lucide Icons:** Clean UI icons.
* **Vanilla CSS Design System:** Glassmorphism, dark mode, smooth micro-animations.

---

## 📁 Project Directory Structure

```text
rag/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI Application entry point & CORS
│   │   ├── core/
│   │   │   └── config.py            # Centralized settings & environment variables
│   │   ├── schemas/
│   │   │   └── chat.py              # Pydantic Request/Response models
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── upload.py        # POST /api/upload endpoint
│   │   │       └── chat.py          # POST /api/chat & GET /api/documents
│   │   └── services/
│   │       ├── pdf_service.py       # PyMuPDF text extraction
│   │       ├── chunking_service.py  # Sliding-window chunker
│   │       ├── embedding_service.py # Vector embedding generator
│   │       ├── vector_service.py    # ChromaDB database client
│   │       └── rag_service.py       # Master RAG pipeline orchestrator
│   ├── tests/
│   │   └── test_rag.py              # Pytest unit & integration tests
│   ├── cli_chatbot.py               # Interactive terminal chatbot
│   ├── test_api.py                  # FastAPI endpoint test script
│   └── requirements.txt             # Python backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx          # Drag & Drop PDF upload + document list
│   │   │   └── ChatArea.jsx         # Chat messages, pills, and sources display
│   │   ├── services/
│   │   │   └── api.js               # Frontend REST API client
│   │   ├── App.jsx                  # Main React application
│   │   └── index.css                # Modern dark-mode glassmorphic styles
│   ├── package.json                 # Frontend dependencies
│   └── vite.config.js               # Vite configuration
│
├── data/
│   └── chroma/                      # Persistent ChromaDB vector storage (git-ignored)
├── uploads/                         # Uploaded PDF document storage (git-ignored)
├── .env.example                     # Environment variable template
├── .gitignore                       # Git security ignore rules
└── README.md                        # Project documentation
```

---

## ⚙️ Prerequisites

Make sure you have the following installed on your machine:
* **Python 3.10 or higher** (`python --version`)
* **Node.js 18 or higher** (`node --version` & `npm --version`)
* **Git** (`git --version`)

---

## 🚀 Setup & Installation (Step-by-Step)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/pdf-rag-chatbot.git
cd pdf-rag-chatbot
```

---

### 2. Configure Environment Variables
Create a `.env` file in the root directory by copying the template:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Open `.env` and enter your **NVIDIA API Key** (you can get a free API key at [build.nvidia.com](https://build.nvidia.com)):

```env
NVIDIA_API_KEY=your_actual_nvidia_api_key_here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL=meta/llama-3.1-70b-instruct
```

---

### 3. Backend Setup

```bash
# 1. Create a Python Virtual Environment
python -m venv backend/venv

# 2. Activate the Virtual Environment
# On Windows (PowerShell):
.\backend\venv\Scripts\Activate.ps1

# On Linux / macOS:
source backend/venv/bin/activate

# 3. Install Backend Dependencies
pip install -r backend/requirements.txt
```

---

### 4. Frontend Setup

In a new terminal window:

```bash
cd frontend
npm install
```

---

## 🏃 Running the Application

### Start the Backend Server (Terminal 1)
```bash
# In project root with venv active:
uvicorn backend.app.main:app --reload --port 8000
```
* **API Documentation & Interactive Swagger UI:** 👉 [`http://localhost:8000/docs`](http://localhost:8000/docs)

### Start the React Web UI (Terminal 2)
```bash
cd frontend
npm run dev
```
* **Open the Web Application:** 👉 [`http://localhost:5173`](http://localhost:5173)

---

## 💻 Optional: Interactive CLI Chatbot (Terminal-Only)

If you prefer testing directly in your terminal without opening a browser:

```bash
python backend/cli_chatbot.py
```

---

## 🧪 Running the Automated Tests

Run the full Pytest test suite (7/7 tests covering Chunking, Embeddings, ChromaDB, Multi-PDF filtering, and Error Handling):

```bash
python -m pytest backend/tests/test_rag.py -v
```

Run the FastAPI Endpoint Integration Test:

```bash
python backend/test_api.py
```

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/upload` | Upload and index any multi-page `.pdf` into ChromaDB |
| `POST` | `/api/chat` | Ask questions and receive grounded LLM answers with sources |
| `GET` | `/api/documents` | List all uploaded PDF filenames |
| `GET` | `/api/health` | Health check & total vector chunks indexed |
| `GET` | `/docs` | Interactive Swagger UI for testing endpoints |

---

## 🛡️ Security Best Practices

* **No Hardcoded Secrets:** All API keys are loaded strictly from environment variables via `.env`.
* **Git Protection:** `.gitignore` ensures that `.env`, `backend/venv/`, `uploads/`, `data/chroma/`, and `node_modules/` are never committed.
* **File Validation:** Restricts uploads to `.pdf` format and validates file size.

---

## 📜 License
This project is open-source under the **MIT License**.
