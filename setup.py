from setuptools import setup, find_packages

setup(
    name="medical_chatbot_llms_groq",
    version="0.1.0",
    description="A Medical Chatbot using LLMs and Groq",
    author="Mohd Fahad Chougle",
    author_email="fahadchougle020304@gmail.com",
    packages=find_packages(),
    install_requires=[
        "langchain-groq",
        "langchain==0.3.26",
        "sentence-transformers==4.1.0",
        "pypdf==5.6.1",
        "python-dotenv==1.1.0",
        "langchain-community==0.3.26",
        "fastapi==0.115.0",
        "uvicorn==0.32.0",
        "chromadb==0.5.17",
        "faiss-cpu"
    ]
)
