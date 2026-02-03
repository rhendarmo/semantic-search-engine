# 🎬 Movie Semantic Search App (RAG-powered)

A production-ready semantic search web application that allows users to search and ask questions about movies using vector embeddings and LLM-powered question answering.

This project uses:
- TMDb API for movie data  
- Sentence Transformers for embeddings  
- FastAPI for backend API  
- Next.js for frontend UI  
- LLM integration for answering questions based on retrieved results (RAG)

Users can:
- Search movies using natural language (semantic search)
- Retrieve the most relevant movie results
- Ask questions grounded in the retrieved movie data (Q&A)
- View similarity scores and movie metadata

---

## 🚀 Features

- Semantic search using cosine similarity on embeddings  
- Movie dataset powered by TMDb API  
- Sentence Transformer embeddings (`all-MiniLM-L6-v2`)  
- Question answering using retrieved results (RAG)  
- Modern web UI built with Next.js  
- FastAPI backend with REST endpoints  
- Top-K ranked results with similarity scores  
- Environment variable support for API keys  

---

## 🏗️ Architecture

```
Frontend (Next.js)
     |
     v
Backend API (FastAPI)
     |
     v
Embedding Model (Sentence Transformers)
     |
     v
Vector Store (NumPy / SQLite / FAISS)
     |
     v
LLM (Q&A based on retrieved chunks)
```

---

## 📁 Project Structure

```
movie-semantic-search/
│
├── backend/
│   ├── app.py
│   ├── embed_corpus.py
│   ├── search.py
│   ├── llm.py
│   ├── data/
│   └── requirements.txt
│
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── styles/
│   └── package.json
│
├── README.md
└── .env
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-semantic-search.git
cd movie-semantic-search
```

---

### 2. Backend Setup (FastAPI)

Create a virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TMDB_API_KEY=your_tmdb_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Run backend server:

```bash
uvicorn app:app --reload
```

Backend will run at:
```
http://localhost:8000
```

Swagger docs:
```
http://localhost:8000/docs
```

---

### 3. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:3000
```

---

## 🧪 Example Usage

### Semantic Search Query

Input:
```
romantic movies about time travel
```

---

### Question Answering (RAG)

Question:
```
Which of these movies has the highest user rating?
```

---

## 🔌 API Endpoints

### Search Movies
POST /search

---

### Ask Question (Q&A)
POST /llm/qa

---

## 🧠 Embedding Model

Using:
- sentence-transformers/all-MiniLM-L6-v2

---

## 🌍 Deployment (Optional)

- Backend: Render / Railway / Fly.io  
- Frontend: Vercel  

---

## 📌 Future Improvements

- Add filters (genre, year, rating)  
- Add user accounts  
- Save search history  
- Add comparative analysis feature  
- Replace NumPy with FAISS or pgvector  
