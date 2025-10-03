from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from src.helper import load_pdf_file, filter_minimal_docs, text_split, download_embeddings
from store_index import build_or_load_faiss_index
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# ---------------- ENV + APP ---------------- #
load_dotenv()
app = FastAPI()

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------- EMBEDDINGS + INDEX ---------------- #
embeddings = download_embeddings()

extracted_data = load_pdf_file("data/")
filtered_data = filter_minimal_docs(extracted_data)
text_chunks = text_split(filtered_data)

docsearch = build_or_load_faiss_index(text_chunks, embeddings)

# ---------------- LLM ---------------- #
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- ROUTES ---------------- #
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the frontend chat page"""
    return templates.TemplateResponse("index.html", {"request": request})


class ChatRequest(BaseModel):
    query: str   # incoming JSON { "query": "your question" }

@app.post("/chat")
async def chat(req: ChatRequest):
    # Retrieve context from FAISS
    results = docsearch.similarity_search(req.query, k=3)
    context = " ".join([doc.page_content for doc in results])

    # Answer with Groq LLM
    response = llm.invoke(f"Context: {context}\n\nQuestion: {req.query}")
    return {"answer": response.content}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render provides PORT env variable
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)

