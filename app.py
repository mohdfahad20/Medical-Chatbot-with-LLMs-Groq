import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from config import *
from rate_limiter import init_rate_limit_db, get_user_identifier, check_rate_limit, get_user_stats

load_dotenv()
init_rate_limit_db()

st.set_page_config(
    page_title=CHAT_TITLE,
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;}
    .source-box {background-color: #f0f2f6; padding: 0.5rem; border-radius: 0.3rem; margin-top: 0.5rem; font-size: 0.85rem;}
    .warning-box {background-color: #ffe5e5; border-left: 4px solid #dc3545; padding: 1rem; margin: 1rem 0; color: #721c24;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialization_done" not in st.session_state:
    st.session_state.initialization_done = False
if "is_initializing" not in st.session_state:
    st.session_state.is_initializing = False
if "docsearch" not in st.session_state:
    st.session_state.docsearch = None
if "llm" not in st.session_state:
    st.session_state.llm = None
if "user_id" not in st.session_state:
    st.session_state.user_id = get_user_identifier()
if "show_sources" not in st.session_state:
    st.session_state.show_sources = INCLUDE_SOURCES

@st.cache_resource(show_spinner=False)
def initialize_models():
    """Initialize models with better error handling"""
    print("🔄 Starting initialization...")
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_groq import ChatGroq
        
        if os.path.exists(FAISS_INDEX_PATH):
            print(f"📂 Loading existing FAISS index from {FAISS_INDEX_PATH}...")
            from langchain_community.embeddings import HuggingFaceEmbeddings
            
            embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            docsearch = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
            print("✅ FAISS index loaded from disk")
        else:
            print("🔨 Building new FAISS index (first time only)...")
            from src.helper import load_pdf_file, filter_minimal_docs, text_split, download_embeddings
            
            embeddings = download_embeddings()
            print("✅ Embeddings model loaded")
            
            extracted_data = load_pdf_file("data/")
            filtered_data = filter_minimal_docs(extracted_data)
            text_chunks = text_split(filtered_data)
            print("✅ PDFs processed")
            
            docsearch = FAISS.from_documents(documents=text_chunks, embedding=embeddings)
            docsearch.save_local(FAISS_INDEX_PATH)
            print("✅ FAISS index created and saved")
        
        print("🤖 Initializing LLM...")
        llm_kwargs = {
            "model": LLM_MODEL,
            "api_key": st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY")),
            "temperature": 0.3
        }
        if MAX_RESPONSE_TOKENS is not None:
            llm_kwargs["max_tokens"] = MAX_RESPONSE_TOKENS
        
        llm = ChatGroq(**llm_kwargs)
        print("✅ LLM ready")
        print("🎉 All systems ready!")
        
        return docsearch, llm, True
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return None, None, False
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        import traceback
        traceback.print_exc()
        return None, None, False

def validate_query(query: str) -> tuple[bool, str]:
    """Validate user query"""
    query = query.strip()
    if len(query) < MIN_QUERY_LENGTH:
        return False, f"Please enter at least {MIN_QUERY_LENGTH} characters"
    if len(query) > MAX_QUERY_LENGTH:
        return False, f"Question too long. Please keep it under {MAX_QUERY_LENGTH} characters"
    return True, ""

def build_context_with_memory(current_query: str, messages: list, context: str) -> str:
    """Add conversation memory to context"""
    if len(messages) > 0:
        recent = messages[-4:]  # Last 2 exchanges
        history = "\n".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in recent])
        return f"Recent conversation:\n{history}\n\nDocument context:\n{context}\n\nCurrent question: {current_query}"
    return f"Document context:\n{context}\n\nQuestion: {current_query}"

def log_interaction(query: str, success: bool, response_time: float):
    """Log interaction for analytics"""
    print(f"[ANALYTICS] {datetime.now().isoformat()} | Query: {len(query)} chars | Success: {success} | Time: {response_time:.2f}s")

# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.title(CHAT_TITLE)
    st.caption(CHAT_SUBTITLE)
with col2:
    st.markdown("✅ **Ready**" if st.session_state.initialization_done else "⏳ **Loading...**")

# Medical Disclaimer
with st.expander("⚠️ Important Medical Disclaimer - Please Read"):
    st.markdown("""
    **This chatbot is for informational and educational purposes only.**
    
    - This is NOT a substitute for professional medical advice, diagnosis, or treatment
    - Always consult a qualified healthcare professional for medical concerns
    - Do not use this tool for medical emergencies - call emergency services immediately
    - The information provided may not be accurate, complete, or up-to-date
    - This is an AI system and can make mistakes
    
    By using this chatbot, you acknowledge these limitations.
    """)

# Initialize models
if not st.session_state.initialization_done and not st.session_state.is_initializing:
    st.session_state.is_initializing = True
    
    with st.spinner(""):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Loading embeddings model...")
        progress_bar.progress(25)
        
        try:
            docsearch, llm, success = initialize_models()
            progress_bar.progress(75)
            status_text.text("✅ Models loaded successfully!")
            
            if success:
                st.session_state.docsearch = docsearch
                st.session_state.llm = llm
                st.session_state.initialization_done = True
                progress_bar.progress(100)
                time.sleep(1)
                status_text.empty()
                progress_bar.empty()
                st.rerun()
            else:
                st.error("Failed to initialize models. Please refresh the page.")
        except Exception as e:
            st.error(f"❌ Error loading models: {e}")
        finally:
            st.session_state.is_initializing = False

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources if enabled and available
        if (message["role"] == "assistant" and 
            "sources" in message and 
            st.session_state.show_sources and 
            message["sources"]):
            with st.expander("📚 View Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {i}:** {source['file']}")
                    st.text(source["text"][:200] + "...")

# Chat input
if prompt := st.chat_input("Type your medical question here...", disabled=not st.session_state.initialization_done):
    
    # Validate query
    is_valid, error_msg = validate_query(prompt)
    if not is_valid:
        st.warning(error_msg)
        st.stop()
    
    # Check rate limit
    user_id = st.session_state.user_id
    can_proceed, requests_made, reset_time = check_rate_limit(user_id, max_requests=RATE_LIMIT_MAX_REQUESTS, window_hours=RATE_LIMIT_WINDOW_HOURS)
    
    if not can_proceed:
        st.error(f"⚠️ Rate limit exceeded!")
        if reset_time:
            st.warning(f"You've made {requests_made} requests in the last {RATE_LIMIT_WINDOW_HOURS} hours. Your access will resume at **{reset_time.strftime('%I:%M %p on %B %d')}**")
        else:
            st.warning(f"You've made {requests_made} requests. Please wait before trying again.")
        st.info("This limit helps ensure fair access for all users and protects API quotas.")
        st.stop()
    
    # Limit chat history
    if len(st.session_state.messages) >= MAX_CHAT_HISTORY:
        st.session_state.messages = st.session_state.messages[-MAX_CHAT_HISTORY:]
    
    timestamp = datetime.now().strftime("%H:%M")
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        start_time = time.time()
        
        try:
            from src.prompt import system_prompt
            
            # Search FAISS
            with st.spinner("🔍 Searching documents..."):
                results = st.session_state.docsearch.similarity_search_with_score(prompt, k=SIMILARITY_TOP_K)
            
            # Filter by relevance
            relevant_docs = [(doc, score) for doc, score in results if score >= MIN_RELEVANCE_SCORE]
            
            if not relevant_docs:
                response_text = "I don't have relevant information about this in my knowledge base. Please consult a healthcare professional for accurate medical information."
                sources = []
            else:
                # Build context with memory
                context = "\n\n".join([doc.page_content for doc, _ in relevant_docs])
                full_context = build_context_with_memory(prompt, st.session_state.messages[:-1], context)
                
                # Generate response with streaming
                full_prompt = system_prompt.format(context=full_context)
                
                message_placeholder = st.empty()
                full_response = ""
                
                with st.spinner("🤔 Generating response..."):
                    try:
                        for chunk in st.session_state.llm.stream(full_prompt):
                            full_response += chunk.content
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                    except:
                        response = st.session_state.llm.invoke(full_prompt)
                        full_response = response.content
                        message_placeholder.markdown(full_response)
                
                response_text = full_response
                sources = [{"file": doc.metadata.get("source", "Unknown"), "text": doc.page_content} for doc, _ in relevant_docs]
            
            response_time = time.time() - start_time
            log_interaction(prompt, True, response_time)
            
        except Exception as e:
            response_text = f"Sorry, I encountered an error: {str(e)}"
            sources = []
            response_time = time.time() - start_time
            log_interaction(prompt, False, response_time)
            st.error(response_text)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response_text, "timestamp": timestamp, "sources": sources})
    st.rerun()

# Sidebar
with st.sidebar:
    st.header("📊 Information")
    
    # Status
    if st.session_state.initialization_done:
        st.success("✅ AI Models Ready")
    elif st.session_state.is_initializing:
        st.warning("⏳ Loading Models...")
    else:
        st.info("🔄 Initializing...")
    
    # Stats
    st.markdown("### 📈 Session Stats")
    total_messages = len(st.session_state.messages)
    user_questions = len([m for m in st.session_state.messages if m["role"] == "user"])
    requests_in_window = get_user_stats(st.session_state.user_id, window_hours=RATE_LIMIT_WINDOW_HOURS)
    requests_remaining = max(0, RATE_LIMIT_MAX_REQUESTS - requests_in_window)
    
    col1, col2 = st.columns(2)
    col1.metric("Messages", total_messages)
    col2.metric("Questions", user_questions)
    
    st.metric("Requests Remaining", f"{requests_remaining}/{RATE_LIMIT_MAX_REQUESTS}")
    st.caption(f"Resets every {RATE_LIMIT_WINDOW_HOURS} hours")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    st.session_state.show_sources = st.checkbox("Show Sources", value=st.session_state.show_sources)
    
    # Actions
    st.markdown("### 🎛️ Actions")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🔄 Restart App", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()
    
    # About
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(f"""
    **Tech Stack:**
    - LLM: {LLM_MODEL}
    - Embeddings: {EMBEDDING_MODEL}
    - Vector DB: FAISS
    - Framework: Streamlit
    
    **Version:** 1.0.0
    """)
    
    st.caption("Built with ❤️ using Streamlit & HF Spaces")

# Footer
st.markdown("---")
st.markdown('<div class="warning-box">⚠️ <strong>Remember:</strong> This is an AI assistant for educational purposes. Always consult qualified healthcare professionals for medical advice.</div>', unsafe_allow_html=True)