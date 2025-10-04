from langchain_community.vectorstores import FAISS
import os


def build_or_load_faiss_index(texts_chunk, embedding, index_path="faiss_index"):
    """
    Create or load a FAISS index for document retrieval.
   
    If the index exists, it loads it. Otherwise, it builds a new one,
    saves it, and returns the FAISS vector store.
    """
    if os.path.exists(index_path):
        print(f"📂 Loading existing FAISS index from {index_path}")
        return FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
    else:
        print(f"🔨 Building new FAISS index at {index_path}")
        docsearch = FAISS.from_documents(documents=texts_chunk, embedding=embedding)
        docsearch.save_local(index_path)
        return docsearch