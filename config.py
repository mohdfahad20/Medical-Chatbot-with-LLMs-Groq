# config.py - Configuration settings for Medical Chatbot

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"
FAISS_INDEX_PATH = "faiss_index"

# Query Settings
MAX_QUERY_LENGTH = 500
MIN_QUERY_LENGTH = 3
SIMILARITY_TOP_K = 5
MIN_RELEVANCE_SCORE = 0.3

# Rate Limiting
RATE_LIMIT_MAX_REQUESTS = 10
RATE_LIMIT_WINDOW_HOURS = 3  # 3 hours instead of 10 minutes

# UI Settings
CHAT_TITLE = "🏥 Medical Chatbot"
CHAT_SUBTITLE = "Ask me medical questions based on trusted documents"
MAX_CHAT_HISTORY = 50

# Response Settings
MAX_RESPONSE_TOKENS = 4096
INCLUDE_SOURCES = True