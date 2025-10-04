from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# ---------------- ENV + APP ---------------- #
load_dotenv()
app = FastAPI()

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------- GLOBALS (lazy init) ---------------- #
docsearch = None
llm = None
initialization_done = False
is_initializing = False


async def initialize_models():
    """Initialize models AFTER server starts - load existing FAISS index"""
    global docsearch, llm, initialization_done, is_initializing
    
    if initialization_done or is_initializing:
        return
    
    is_initializing = True
    print("🔄 Starting initialization...")
    
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_groq import ChatGroq
        
        # Check if FAISS index exists
        if os.path.exists("faiss_index"):
            print("📂 Loading existing FAISS index...")
            # Import lightweight embeddings only for loading
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
            # Fallback: build new index (only if doesn't exist)
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
            api_key=os.getenv("GROQ_API_KEY")
        )
        print("✅ LLM ready")
        
        initialization_done = True
        is_initializing = False  # CRITICAL: Set to False when done!
        print("🎉 All systems ready!")
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        import traceback
        traceback.print_exc()
        is_initializing = False
        initialization_done = False
        raise


# ---------------- ROUTES ---------------- #
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the frontend chat page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_ready": initialization_done,
        "initializing": is_initializing
    }


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
async def chat(req: ChatRequest):
    global docsearch, llm
    
    # Check if initialized
    if not initialization_done:
        if not is_initializing:
            import asyncio
            asyncio.create_task(initialize_models())
        return {
            "answer": "🔄 Loading AI models for the first time... Please try again in 15-20 seconds!",
            "status": "initializing"
        }
    
    if is_initializing:
        return {
            "answer": "⏳ Still loading models... Please wait a moment.",
            "status": "initializing"
        }
    
    try:
        # Import custom prompt
        from src.prompt import system_prompt
        
        # Use FAISS for semantic search
        results = docsearch.similarity_search(req.query, k=3)
        context = "\n\n".join([doc.page_content for doc in results])
        
        # Use your custom system prompt
        prompt = system_prompt.format(context=context) + f"\n\nQuestion: {req.query}\n\nAnswer:"
        
        response = llm.invoke(prompt)
        return {"answer": response.content, "status": "success"}
    
    except Exception as e:
        print(f"Error in chat: {e}")
        return {
            "answer": f"Sorry, I encountered an error: {str(e)}",
            "status": "error"
        }


@app.on_event("startup")
async def startup_event():
    """Start initialization after server is up"""
    import asyncio
    await asyncio.sleep(2)  # Let server fully start first
    asyncio.create_task(initialize_models())
    print("🚀 Server started! Initializing in background...")


# ---------------- RENDER DEPLOYMENT ---------------- #
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)