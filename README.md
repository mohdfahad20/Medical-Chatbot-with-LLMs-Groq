<!--
---
title: Medical Chatbot Using LLM 
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.40.0
app_file: app.py
pinned: false
license: apache-2.0
---
-->

# Medical Chatbot Using LLM

An AI-powered medical assistant that provides information from medical documents using RAG (Retrieval Augmented Generation), semantic search, and large language models.

[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/VeNoM21/medical-chatbot)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

---

## ✨ Features

- 🔍 **Semantic Search** - FAISS vector database for intelligent document retrieval
- 🤖 **Powered by Groq** - Fast LLM inference using Llama 3.1-8b-instant
- 💬 **Interactive Chat** - Clean Streamlit interface with conversation memory
- 🛡️ **Rate Limiting** - Fair usage protection (10 requests per 3 hours)
- 📚 **Source Citations** - Toggle to view document sources for responses
- ⚡ **Fast Initialization** - Pre-built embeddings for quick startup
- 🔒 **Safety First** - Built-in medical disclaimers and responsible AI practices

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit |
| **LLM Provider** | Groq (Llama 3.1-8b-instant) |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **Rate Limiting** | SQLite |
| **Document Processing** | LangChain, PyPDF |
| **Hosting** | Hugging Face Spaces |

---

## 🚀 Quick Start

### Option 1: Use Online

Visit the live demo: **[HF Spaces](https://huggingface.co/spaces/VeNoM21/Medical-Chatbot-Using-LLM)**

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/mohdfahad20/Medical-Chatbot-with-LLMs-Groq.git
cd Medical-Chatbot-with-LLMs-Groq

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Run the application
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

**Get Groq API Key:** [console.groq.com](https://console.groq.com)

---

## 📁 Project Structure

```
medical-chatbot/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration settings
├── rate_limiter.py        # Rate limiting logic (SQLite)
├── requirements.txt       # Python dependencies
├── LICENSE               # MIT License
├── README.md            # Documentation
├── .env                 # Environment variables (not in repo)
├── .gitignore          # Git ignore rules
│
├── .streamlit/
│   └── config.toml     # Streamlit theme configuration
│
├── src/
│   ├── prompt.py       # Custom system prompt template
│   └── helper.py       # Utility functions (PDF loading, text splitting)
│
├── faiss_index/        # Pre-built FAISS vector index
│   ├── index.faiss     # Vector embeddings
│   └── index.pkl       # Metadata
│
├── data/              # Medical PDF documents
│   └── Medical_book.pdf
│
└── archive/           # Archived old files (not deployed)
    ├── app_fastapi_backup.py
    ├── requirements_fastapi.txt
    ├── static/
    └── templates/
```

---

## 🔧 Configuration

### Environment Variables

**Required:**
- `GROQ_API_KEY` - Your Groq API key for LLM access

**For Hugging Face Spaces:**
Add secrets in: `Settings → Variables and secrets → New secret`

### Key Settings (config.py)

```python
# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"

# Rate Limiting
RATE_LIMIT_MAX_REQUESTS = 10
RATE_LIMIT_WINDOW_HOURS = 3

# Query Settings
MAX_QUERY_LENGTH = 500
MIN_QUERY_LENGTH = 3
SIMILARITY_TOP_K = 5
```

---

## 📖 How It Works

```
User Query
    ↓
1. Validate Input (length, rate limit check)
    ↓
2. Generate Query Embedding (sentence-transformers)
    ↓
3. Search FAISS Index (similarity search, top 5 results)
    ↓
4. Build Context (relevant chunks + conversation history)
    ↓
5. Send to Groq LLM (Llama 3.1 + system prompt)
    ↓
6. Stream Response (word-by-word display)
    ↓
7. Display Answer (with optional source citations)
```

---

## ⚠️ Important Disclaimers

### Medical Disclaimer

**THIS CHATBOT IS FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

- ❌ NOT a substitute for professional medical advice, diagnosis, or treatment
- ❌ NOT for medical emergencies - call emergency services immediately
- ✅ Always consult qualified healthcare professionals for medical concerns
- ⚠️ Information may not be accurate, complete, or up-to-date
- 🤖 This is an AI system and can make mistakes

### Usage Limitations

- **Rate Limit:** 10 requests per 3 hours per user session
- **Best For:** General medical information and education
- **Not For:** Diagnosis, treatment recommendations, emergency situations

---

## 🔐 Privacy & Data

- ✅ No user data is permanently stored
- ✅ Queries are logged temporarily for rate limiting only
- ✅ Rate limit data resets every 3 hours
- ✅ SQLite database is session-based (not persistent across deployments)
- 📝 **Future Enhancement:** MongoDB integration for persistent rate limiting

---

## 🚧 Known Limitations

1. **Session-Based Rate Limiting** - Resets on page refresh (SQLite limitation)
2. **Response Length** - Very long queries may get truncated due to token limits
3. **Single PDF Source** - Currently processes one medical document
4. **No User Authentication** - Anyone can access (free tier constraint)

---

## 🎯 Future Enhancements

- [ ] MongoDB integration for persistent rate limiting across sessions
- [ ] Multiple PDF document support
- [ ] User authentication system
- [ ] Conversation export (download chat history)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Built by:** Mohd Fahad
**GitHub:** [mohdfahad20](https://github.com/mohdfahad20/)  
**Purpose:** Educational project demonstrating RAG with LLMs

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) - RAG framework and document processing
- [Groq](https://groq.com) - Ultra-fast LLM inference
- [Hugging Face](https://huggingface.co) - Free hosting and ML infrastructure
- [Streamlit](https://streamlit.io) - Rapid web app development
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/mohdfahad20/Medical-Chatbot-with-LLMs-Groq/issues)
- **HF Space:** [VeNoM21/Medical-Chatbot-Using-LLM](https://huggingface.co/spaces/VeNoM21/Medical-Chatbot-Using-LLM)

---

## 📊 Project Stats

**Last Updated:** October 2025  
**Status:** Active Development

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**