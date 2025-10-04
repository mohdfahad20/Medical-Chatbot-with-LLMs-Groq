from fastapi import FastAPI, Request, BackgroundTasks
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
embeddings = None
docsearch = None
llm = None
is_initializing = False
initialization_done = False


async def initialize_models():
    """Initialize heavy models AFTER server starts"""
    global embeddings, docsearch, llm, is_initializing, initialization_done
    
    if initialization_done or is_initializing:
        return
    
    is_initializing = True
    print("🔄 Starting model initialization (this may take a minute)...")
    
    try:
        # Import heavy libraries only when needed
        from src.helper import load_pdf_file, filter_minimal_docs, text_split, download_embeddings
        from store_index import build_or_load_faiss_index
        from langchain_groq import ChatGroq
        
        embeddings = download_embeddings()
        print("✅ Embeddings loaded")
        
        extracted_data = load_pdf_file("data/")
        filtered_data = filter_minimal_docs(extracted_data)
        text_chunks = text_split(filtered_data)
        print("✅ PDFs processed")
        
        docsearch = build_or_load_faiss_index(text_chunks, embeddings)
        print("✅ FAISS index ready")
        
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )
        print("✅ LLM initialized")
        
        initialization_done = True
        print("🎉 All models ready!")
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        is_initializing = False
        raise


# ---------------- ROUTES ---------------- #
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the frontend chat page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    """Health check endpoint - shows if models are ready"""
    return {
        "status": "healthy",
        "models_ready": initialization_done,
        "initializing": is_initializing
    }


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
async def chat(req: ChatRequest, background_tasks: BackgroundTasks):
    global embeddings, docsearch, llm
    
    # Start initialization in background if not done
    if not initialization_done and not is_initializing:
        background_tasks.add_task(initialize_models)
        return {
            "answer": "🔄 Models are loading, please try again in 30 seconds...",
            "status": "initializing"
        }
    
    if is_initializing:
        return {
            "answer": "⏳ Models are still loading, please wait...",
            "status": "initializing"
        }
    
    if not initialization_done:
        return {
            "answer": "❌ Models failed to initialize. Please contact support.",
            "status": "error"
        }
    
    try:
        # Retrieve context from FAISS
        results = docsearch.similarity_search(req.query, k=3)
        context = " ".join([doc.page_content for doc in results])
        
        # Answer with Groq LLM
        response = llm.invoke(f"Context: {context}\n\nQuestion: {req.query}")
        return {"answer": response.content, "status": "success"}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "status": "error"}


@app.on_event("startup")
async def startup_event():
    """Start model loading in background after server starts"""
    import asyncio
    asyncio.create_task(initialize_models())


# ---------------- RENDER DEPLOYMENT ---------------- #
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)