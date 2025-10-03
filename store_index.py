from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_minimal_docs, text_split, download_embeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


extracted_data=load_pdf_file(data='data/')
filter_data = filter_minimal_docs(extracted_data)
text_chunks=text_split(filter_data)

embeddings = download_embeddings()


def build_or_load_faiss_index(texts_chunk, embedding, index_path="faiss_index"):
    
    """
    Create or load a FAISS index for document retrieval.
    
    If the index exists, it loads it. Otherwise, it builds a new one,
    saves it, and returns the FAISS vector store.
    """

    if os.path.exists(index_path):
        return FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
    else:
        docsearch = FAISS.from_documents(documents=texts_chunk, embedding=embedding)
        docsearch.save_local(index_path)
        return docsearch
    

docsearch = build_or_load_faiss_index(text_chunks, embeddings)
