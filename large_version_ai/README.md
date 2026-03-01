# Automotive RAG API (Flask + LangChain + FAISS + Ollama)

A Flask backend that exposes a **/api/chat** endpoint to answer user questions about automotive datasets stored in **Excel files** using **RAG (Retrieval-Augmented Generation)**.

The server:
- Loads **two Excel knowledge bases** into **FAISS** vector stores
- Uses **HuggingFace embeddings** (`all-MiniLM-L6-v2`)
- Calls a **local LLM via Ollama** (`phi3`)
- Lets the frontend choose between **3 “modes”** (`model`) that change prompting behavior

---

## ✨ Features

- ✅ **RAG over Excel**: retrieve relevant rows/text from `.xlsx` and answer from that context
- ✅ **Two knowledge bases**:
  - `big_data_voiture.xlsx` (used by model1 & model3 in code)
  - `data.xlsx` (used by model2 in code; fallback to the first file if missing)
- ✅ **Frontend model selector** (`model` in request JSON):
  - `gpt-4` → short, friendly assistant
  - `codex-v2` → strict **data analyst** (facts + calculations only, no code)
  - `creative-x` → simple calculations + may show basic pandas/matplotlib examples
- ✅ **Runs on port 8080** (public-ready with `0.0.0.0`)

---

## 📁 Project Structure (recommended)

```bash
large_version_ai/
│-- chat_ai_app.py                    
│-- main.py                   
│-- big_data_voiture.xlsx      # Excel knowledge base 1 (required)
│-- data.xlsx                  # Excel knowledge base 2 (optional; fallback enabled)
│-- requirements.txt           # Python dependencies
│-- .gitignore
└-- README.md