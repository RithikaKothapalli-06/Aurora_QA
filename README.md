# AURORA QA SYSTEM 
Natural-language question answering over member messages using semantic search + lightweight reasoning.

## 🚀 Overview
This project implements a small production-ready API service that answers natural-language questions such as:

- “When is Layla planning her trip?”
- “How many cars does Vikram Desai have?”
- “What are Amira’s favorite restaurants?”

The system retrieves messages from the public November API and performs semantic search + rule-based reasoning to generate an answer.  
It is deployed as a FastAPI service with one main endpoint:
GET /ask?question=your_question

---

# 🧠 Architecture

### 1. **Data Fetching**
We collect messages from:
GET /messages

Messages are cleaned, normalized, and cached locally.

### 2. **Vector Search (FAISS/Chroma)**
- Each message is embedded using MiniLM sentence embeddings.
- The embeddings are stored in a vector index.
- At query time, we retrieve the **top-k semantically similar** messages.

### 3. **Lightweight Reasoning Engine**
Instead of using LLM APIs (not allowed for submission), a simple but effective rule-based engine handles:

- **Count extraction** (“how many …?”)
- **Date identification** (“when …?”)
- **Favorites / preferences**
- **Travel / destination extraction**
- **Fallback semantic relevance**

This allows the system to answer many structured natural-language questions without a hosted LLM.

### 4. **FastAPI Service**
A clean public API exposes:
- `/ask` — ask a natural language question  
- `/` — health check  

Deployed via Render using **Gunicorn + UvicornWorker**.

---

# 🎁 Bonus Goal 1 — Design Notes (Alternative Approaches Considered)

I evaluated several architectures before choosing the final design:

### **Approach A — Full LLM Answering (GPT-4o, Groq, Mixtral)**
**Pros:** Best reasoning, flexible, handles all types of questions  
**Cons:** Requires API keys → not allowed for submission  
**Status:** Not used, but ideal for a production Aurora system.

### **Approach B — Local Mini-LLM (Phi-3, Mistral 7B, Llama 3B locally on CPU)**
**Pros:** No external API  
**Cons:** Too heavy for Render free tier  
**Status:** Not chosen

### **Approach C — RAG + Lightweight Reasoning (Final Choice)**
**Pros:**  
- Fast  
- Works without LLM API keys  
- Cheap to run on Render  
- Deterministic behavior  
- Satisfies all assessment requirements  

**Cons:**  
- Not as flexible as LLMs  
- Hard to answer deeply open-ended questions  

**Status:** Selected as the best balance between reliability, cost, and constraints.

---

# 🎁 Bonus Goal 2 — Data Insights (Anomalies Found)

While analyzing ~1000 messages from the November API, I noticed:

### **1. Duplicate Messages**
Some members post near-identical messages with minor wording changes.

### **2. Inconsistent Formatting**
- Some messages include random line breaks  
- Some contain emojis  
- A few use unusual capitalization  

This required cleaning and normalization.

### **3. Missing or Ambiguous Fields**
- Many messages do not mention explicit dates  
- Some messages reference locations without context (“Going soon!”)  
- Some users mention numbers that are not counts (e.g., “Room 204”)

### **4. No Ground-Truth Labels**
There is no direct structure for:
- trips  
- favorites  
- possessions  
- dates  

This reinforced the decision to use a semantic approach rather than rule-only.

---

# 🛠️ Tech Stack

- **Python 3.12**
- **FastAPI**
- **Uvicorn + Gunicorn**
- **ChromaDB / FAISS**
- **SentenceTransformers MiniLM**
- **Requests**
- **Render (Deployment)**

---

# ▶️ Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs

Ask a question:
GET /ask?question=When is Layla planning her trip?


