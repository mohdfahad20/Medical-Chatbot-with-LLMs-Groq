# Medical Chatbot Using LLM

An AI-powered medical assistant that provides information from medical documents using RAG (Retrieval Augmented Generation), semantic search, and large language models.

[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/VeNoM21/medical-chatbot)
[![Docker Hub](https://img.shields.io/badge/🐳%20Docker-Hub-blue)](https://hub.docker.com/r/mohdfahad21/medical-chatbot)
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
- 🐳 **Docker Ready** - One-command deployment with Docker Compose

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
| **Containerization** | Docker, Docker Compose |
| **Hosting** | Hugging Face Spaces, Docker Hub |

---

## 🚀 Quick Start

### Option 1: Use Online (Easiest)

Visit the live demo: **[Hugging Face Spaces](https://huggingface.co/spaces/VeNoM21/Medical-Chatbot-Using-LLM)**

---

### Option 2: Run with Docker 🐳 (Recommended)

**Prerequisites:**
- Docker & Docker Compose installed ([Get Docker](https://docs.docker.com/get-docker/))
- Groq API Key ([Get free key](https://console.groq.com))

**Steps:**

```bash
# 1. Clone the repository
git clone https://github.com/mohdfahad20/Medical-Chatbot-with-LLMs-Groq.git
cd Medical-Chatbot-with-LLMs-Groq

# 2. Create .env file
cp .env

# 3. Edit .env and add your Groq API key
# Use any text editor: nano .env, vim .env, or VS Code
# Replace: GROQ_API_KEY=your_groq_api_key_here

# 4. Run with Docker Compose (that's it!)
docker-compose up

# The app will be available at: http://localhost:8501
```

**To stop the app:**
```bash
# Press Ctrl+C in the terminal
# Or run:
docker-compose down
```

**Why Docker Compose?** It automates everything - pulls the image, sets up environment variables, configures ports, and starts the app. No complex commands needed!

---

### Option 3: Run Locally (Without Docker)

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

---

## 🐳 Docker Details

### Using Pre-built Image from Docker Hub

The easiest way to run the app:

```bash
# Pull the latest image
docker pull mohdfahad21/medical-chatbot:latest

# Run with your API key
docker run -p 8501:8501 -e GROQ_API_KEY=your_key_here mohdfahad21/medical-chatbot:latest
```

### Building Locally

If you want to build from source:

```bash
# Build the Docker image
docker build -t medical-chatbot:latest .

# Run the container
docker run -p 8501:8501 --env-file .env medical-chatbot:latest
```

### Docker Compose Benefits

The `docker-compose.yml` file simplifies everything:
- ✅ Automatic port mapping (8501:8501)
- ✅ Environment variable loading from `.env`
- ✅ Container restart on failure
- ✅ Health checks
- ✅ Single command to start/stop

**Common Docker Compose Commands:**
```bash
# Start in foreground
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the app
docker-compose down

# Rebuild and start
docker-compose up --build
```

---

## 📁 Project Structure

```
medical-chatbot/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration settings
├── rate_limiter.py        # Rate limiting logic (SQLite)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker build exclusions
├── .env.example         # Environment variables template
├── LICENSE              # Apache 2.0 License
├── README.md           # Documentation
├── .env                # Your API keys (not in repo)
├── .gitignore         # Git ignore rules
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

**Setup Steps:**

1. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your API key:**
   ```bash
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

3. **Get your Groq API key:**
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up (free)
   - Navigate to API Keys
   - Create new API key
   - Copy and paste into `.env`

**⚠️ Important:** Never commit `.env` to GitHub - it's already in `.gitignore`

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

## 🐛 Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 instead of 8501
```

**Container won't start:**
```bash
# Check logs
docker-compose logs -f

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

**API Key not working:**
- Verify `.env` file is in the same directory as `docker-compose.yml`
- Check that there are no extra spaces around the `=` in `.env`
- Ensure your API key is valid at [console.groq.com](https://console.groq.com)

**Image size concerns:**
- Pre-built image: ~1.5-2GB (optimized with CPU-only PyTorch)
- This is normal for ML applications with embeddings models

---

## 🎯 Future Enhancements

- [ ] MongoDB integration for persistent rate limiting across sessions
- [ ] Multiple PDF document support
- [ ] User authentication system
- [ ] Conversation export (download chat history)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

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
**Docker Hub:** [mohdfahad21](https://hub.docker.com/u/mohdfahad21)  
**Purpose:** Educational project demonstrating RAG with LLMs

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) - RAG framework and document processing
- [Groq](https://groq.com) - Ultra-fast LLM inference
- [Hugging Face](https://huggingface.co) - Free hosting and ML infrastructure
- [Streamlit](https://streamlit.io) - Rapid web app development
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search
- [Docker](https://docker.com) - Containerization platform

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/mohdfahad20/Medical-Chatbot-with-LLMs-Groq/issues)
- **Hugging Face Space:** [VeNoM21/Medical-Chatbot-Using-LLM](https://huggingface.co/spaces/VeNoM21/Medical-Chatbot-Using-LLM)
- **Docker Hub:** [mohdfahad21/medical-chatbot](https://hub.docker.com/r/mohdfahad21/medical-chatbot)

---

## 📊 Project Stats

**Last Updated:** October 2025  
**Status:** Active Development  
**Docker Support:** ✅ Available  
**Version:** 1.0.0

---

## 🌟 Quick Start Summary

**Fastest way to run:**
```bash
git clone https://github.com/mohdfahad20/Medical-Chatbot-with-LLMs-Groq.git
cd Medical-Chatbot-with-LLMs-Groq
cp .env.example .env
# Edit .env with your GROQ_API_KEY
docker-compose up
# Open http://localhost:8501
```

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**