# TEAM_CONTRIBUTIONS

This document outlines the individual contributions of each team member to the Semantic Search Engine project. All members collaborated throughout the project lifecycle, including design discussions, testing, debugging, and final integration.

---

## Team Member 1: Raditya Hendarmo
**Primary Responsibilities**
- Designed and implemented the core **semantic search pipeline** using sentence-transformer embeddings.
- Implemented **cosine similarity ranking** and Top-K retrieval logic.
- Structured backend search responses to return similarity scores and movie metadata.

**Key Contributions**
- Search quality and relevance
- Embedding consistency between corpus and queries
- Backend logic for retrieval performance

---

## Team Member 2: Gloria Huang
**Primary Responsibilities**
- Developed the **FastAPI backend** and RESTful endpoints.
- Implemented request validation, error handling, and environment variable management.
- Integrated TMDb API data access and backend configuration.

**Key Contributions**
- API design (`/search`, `/llm/qa`)
- Backend reliability and maintainability
- Local development and debugging support

---

## Team Member 3: Kyle Biagan
**Primary Responsibilities**
- Built the **LLM-enhanced Q&A (RAG) pipeline**.
- Designed prompts to ensure answers are grounded in retrieved movie results.
- Integrated OpenAI (or compatible) API for contextual question answering.

**Key Contributions**
- Retrieval-augmented generation logic
- Prompt engineering and response validation
- Source transparency in Q&A responses

---

## Team Member 4: Luc Teagan White
**Primary Responsibilities**
- Developed the **frontend user interface** using Next.js.
- Implemented search and Q&A input flows and results display.
- Connected frontend components to backend API endpoints.

**Key Contributions**
- User experience and interaction design
- Frontend-backend integration
- UI testing and usability refinement

---

## Team Member 5: Ernesto Mata
**Primary Responsibilities**
- Led **data collection and preprocessing** from the TMDb API.
- Cleaned, normalized, and structured movie metadata for embedding.
- Contributed to documentation and example usage preparation.

**Key Contributions**
- Dataset quality and consistency
- Embedding-ready document construction
- Documentation clarity and example queries

---

## Team Collaboration Notes
- All team members participated in architectural discussions and design decisions.
- Code reviews, testing, and debugging were conducted collaboratively.
- Final documentation, repository organization, and demo preparation were completed as a team.

