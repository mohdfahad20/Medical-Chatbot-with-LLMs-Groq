---
title: Medical Chatbot Using LLM 
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.40.0
app_file: app.py
pinned: false
license: mit
---

# 🏥 Medical Chatbot Using LLM

An AI-powered medical assistant that answers questions based on medical documents using semantic search and large language models.

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/VeNoM21/medical-chatbot)

---

## ✨ Features

- 📚 **Semantic Search**: Uses FAISS vector database for intelligent document retrieval
- 🤖 **LLM-Powered**: Leverages Groq's Llama 3.1 for natural language responses
- 💬 **Chat Interface**: Clean, intuitive Streamlit chat UI
- ⚡ **Fast Responses**: Pre-built embeddings for quick initialization
- 🔒 **Safe & Responsible**: Built-in medical disclaimers

---

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **LLM**: Groq (Llama 3.1-8b-instant)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS
- **Document Processing**: LangChain, PyPDF
- **Hosting**: Hugging Face Spaces

---

## 🚀 Quick Start

### Option 1: Use Online (Recommended)

Visit the live demo: [Hugging Face Space](https://huggingface.co/spaces/VeNoM21/medical-chatbot)

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://huggingface.co/spaces/VeNoM21/medical-chatbot
cd medical-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 📁 Project Structure

```
medical-chatbot/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── src/
│   ├── prompt.py          # Custom system prompt
│   └── helper.py          # Utility functions
├── faiss_index/           # Pre-built FAISS vector index
│   ├── index.faiss
│   └── index.pkl
└── data/                  # Medical PDF documents
    └── *.pdf
```

---

## 🔧 Configuration

### Environment Variables

Required for local development:
- `GROQ_API_KEY`: Your Groq API key ([Get one here](https://console.groq.com))

For Hugging Face Spaces, add this in **Settings → Variables and secrets**

---

## 📖 How It Works

1. **Document Loading**: Medical PDF is processed and split into chunks
2. **Embedding**: Text chunks are converted to vector embeddings
3. **Indexing**: Embeddings are stored in FAISS for fast similarity search
4. **Query Processing**: User questions are embedded and matched against the index
5. **Response Generation**: Relevant context + query sent to Groq LLM
6. **Answer Display**: LLM response shown in chat interface

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This chatbot is for **informational and educational purposes only**. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- Always consult a qualified healthcare professional for medical concerns
- Do not use this tool for medical emergencies
- The information provided may not be accurate or up-to-date
- This is an AI system and can make mistakes

---

## 🤝 Contributing

This is a demo project. For improvements or issues:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👨‍💻 Author

Built with ❤️ for educational purposes

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) for the RAG framework
- [Groq](https://groq.com) for fast LLM inference
- [Hugging Face](https://huggingface.co) for hosting
- [Streamlit](https://streamlit.io) for the UI framework

---

## 📊 Stats

![Space Views](https://huggingface.co/spaces/YOUR_USERNAME/medical-chatbot/badge.svg)

Last Updated: 2025-10-05