# Build-a-Complete-Medical-Chatbot-with-LLMs(Groq)-LangChain-FastAPI/Flask-Chroma/Faiss

---

## 🚀 How to run?

### STEP 01 – Clone the repository

```bash
git clone https://github.com/mohdfahad20/Medical-Chatbot-with-LLMs-Groq.git
```

### STEP 02 – Create a virtual environment (Windows, using `py` launcher)

```bash
py -3.10 -m venv venv
```

### STEP 03 – Activate the environment

```bash
venv\Scripts\activate
```

✅ After this, your shell prompt should change to `(venv)` and you can install requirements with:

```bash
pip install -r requirements.txt
```

---

### STEP 04 – Create a `.env` file in the root directory

Add your **Groq API key** as follows:

```ini
GROQ_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

### STEP 05 – Store embeddings into Chroma/Faiss (depending on which one you choose)

```bash
python store_index.py
```

---

### STEP 06 – Run the chatbot app

(using **FastAPI** or **Flask**, depending on your setup)

```bash
python app.py
```

Now open up your browser at:

```bash
http://127.0.0.1:8000   # (FastAPI with uvicorn)
```

or

```bash
http://127.0.0.1:5000   # (Flask)
```

---

## 🛠️ Techstack Used

* Python
* LangChain
* Groq (LLM API)
* FastAPI / Flask
* ChromaDB / Faiss (Vector DB)

---