# ANALYSE D’UN PARC AUTOMOBILE 🚗📊  
**Deux versions du projet :**
1) **Small Version** : gestion / analyse simple d’une liste de voitures (sans IA)  
2) **Large Version (AI / RAG)** : assistant IA basé sur `big_voiture.xlsx` (LangChain + FAISS + Ollama)

---

## ✅ 1) Project Structure (2 parts)

```bash
analyse-parc-automobile/
│
├── small_version/                      # ✅ Small (liste voitures + analyse simple)
│   ├── app.py                          # API Flask (CRUD/filters/summary) ou logique simple
│   ├── data.xlsx                       # Dataset (parc automobile)
│   ├── requirements.txt                # Dépendances small
│   └── README.md                       # (optionnel) mini doc
│
├── large_version_ai/                   # 🔥 Large (IA + RAG)
│   ├── api_server.py                   # Flask API: /api/chat (RAG)
│   ├── cli_chat.py                     # Script CLI pour poser des questions (RAG)
│   ├── data.xlsx                       # Dataset (parc automobile)
│   ├── requirements.txt                # Dépendances IA
│   └── README.md                       # (optionnel) mini doc
│
└── README.md                            
```
