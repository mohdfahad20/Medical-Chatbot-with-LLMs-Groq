import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS matching your original design
st.markdown("""
<style>
    /* Main chat container */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user-message"] {
        background-color: #dcf8c6;
    }
    
    /* Bot message styling */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #f1f0f0;
    }
    
    /* Header styling */
    .css-1v0mbdj {
        max-width: 800px;
    }
    
    /* Status badge */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .status-ready {
        background-color: #4cd137;
        color: white;
    }
    .status-loading {
        background-color: #ffa502;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
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


@st.cache_resource(show_spinner=False)
def initialize_models():
    """
    Initialize models - cached to run only once
    Matches your FastAPI initialize_models() function
    """
    print("🔄 Starting initialization...")
    
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_groq import ChatGroq
        
        # Check if FAISS index exists
        if os.path.exists("faiss_index"):
            print("📂 Loading existing FAISS index...")
            from langchain_community.embeddings import HuggingFaceEmbeddings
            
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            docsearch = FAISS.load_local(
                "faiss_index", 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            print("✅ FAISS index loaded from disk")
        else:
            # Fallback: build new index
            print("🔨 Building new FAISS index (first time only)...")
            from src.helper import load_pdf_file, filter_minimal_docs, text_split, download_embeddings
            
            embeddings = download_embeddings()
            print("✅ Embeddings model loaded")
            
            extracted_data = load_pdf_file("data/")
            filtered_data = filter_minimal_docs(extracted_data)
            text_chunks = text_split(filtered_data)
            print("✅ PDFs processed")
            
            docsearch = FAISS.from_documents(documents=text_chunks, embedding=embeddings)
            docsearch.save_local("faiss_index")
            print("✅ FAISS index created and saved")
        
        print("🤖 Initializing LLM...")
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        )
        print("✅ LLM ready")
        print("🎉 All systems ready!")
        
        return docsearch, llm, True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        import traceback
        traceback.print_exc()
        raise


# Header with status
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏥 Medical Chatbot")
    st.markdown("Ask me anything about medical topics!")

with col2:
    if st.session_state.initialization_done:
        st.markdown('<span class="status-badge status-ready">✅ Ready</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-loading">⏳ Loading...</span>', unsafe_allow_html=True)

# Initialize models
if not st.session_state.initialization_done and not st.session_state.is_initializing:
    st.session_state.is_initializing = True
    
    with st.spinner("🔄 Loading AI models... This takes about 30 seconds on first run."):
        try:
            docsearch, llm, success = initialize_models()
            st.session_state.docsearch = docsearch
            st.session_state.llm = llm
            st.session_state.initialization_done = True
            st.session_state.is_initializing = False
            st.success("✅ AI models loaded successfully!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error loading models: {e}")
            st.session_state.is_initializing = False
            st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(message["timestamp"])

# Chat input
if prompt := st.chat_input("Type your medical question here...", disabled=not st.session_state.initialization_done):
    
    # Add timestamp
    timestamp = datetime.now().strftime("%H:%M")
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)
    
    # Generate bot response
    with st.chat_message("assistant"):
        
        # Check initialization status (matching FastAPI logic)
        if not st.session_state.initialization_done:
            response_text = "🔄 Loading AI models for the first time... Please try again in 15-20 seconds!"
            st.warning(response_text)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": timestamp
            })
            st.stop()
        
        if st.session_state.is_initializing:
            response_text = "⏳ Still loading models... Please wait a moment."
            st.warning(response_text)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": timestamp
            })
            st.stop()
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            try:
                # Import custom prompt (matching FastAPI)
                from src.prompt import system_prompt
                
                # Search FAISS for relevant documents
                results = st.session_state.docsearch.similarity_search(prompt, k=3)
                context = "\n\n".join([doc.page_content for doc in results])
                
                # Use your custom system prompt
                full_prompt = system_prompt.format(context=context) + f"\n\nQuestion: {prompt}\n\nAnswer:"
                
                # Generate response
                response = st.session_state.llm.invoke(full_prompt)
                response_text = response.content
                
                # Display response
                st.markdown(response_text)
                st.caption(timestamp)
                
                # Log query (matching FastAPI)
                print(f"[{datetime.now()}] User query: {prompt}")
                
            except Exception as e:
                response_text = f"Sorry, I encountered an error: {str(e)}"
                st.error(response_text)
                print(f"Error in chat: {e}")
        
        # Add bot response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": timestamp
        })

# Sidebar (matching your original design)
with st.sidebar:
    st.header("🏥 Medical Assistant")
    
    # Status info
    st.markdown("### 📊 Status")
    if st.session_state.initialization_done:
        st.success("✅ Models Ready")
    elif st.session_state.is_initializing:
        st.warning("⏳ Loading...")
    else:
        st.info("🔄 Initializing...")
    
    # Stats
    st.markdown("### 📈 Stats")
    st.metric("Total Messages", len(st.session_state.messages))
    st.metric("Your Questions", len([m for m in st.session_state.messages if m["role"] == "user"]))
    
    # About section
    st.markdown("### ℹ️ About")
    st.markdown("""
    This chatbot uses:
    - 📚 Medical PDF documents
    - 🔍 FAISS vector search
    - 🤖 Groq LLM (Llama 3.1)
    - 🎯 Semantic similarity matching
    
    **⚠️ Medical Disclaimer:**
    This chatbot provides information for educational purposes only. 
    It is not a substitute for professional medical advice, diagnosis, or treatment.
    Always consult a qualified healthcare professional for medical concerns.
    """)
    
    # Clear chat button
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit & Hugging Face Spaces")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d')}")

# Footer info
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This is an AI assistant for informational purposes only. Always seek professional medical advice.")