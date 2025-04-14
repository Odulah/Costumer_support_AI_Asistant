# Customer Support AI Assistant

## 🔍 Overview
This project is a Retrieval-Augmented Generation (RAG) based AI assistant designed to help answer customer support queries. It retrieves relevant past Q&A data and generates contextual, human-like responses using the Falcon-7B model from Hugging Face.

---

## ✅ Submission Checklist
- [x] Clean, modular GitHub repository ✅
- [x] API endpoint (optional: can be deployed using Replit/Render) ✅
- [x] README and PPT with approach, RAG details, and explainability ✅

---

## 🛠️ Tech Stack
- Python
- FastAPI
- Hugging Face Transformers & Inference API
- FAISS (Facebook AI Similarity Search)
- SentenceTransformers (`all-MiniLM-L6-v2`)

---

## 🧠 Approach Taken
1. **Data Loading & Cleaning:**
   - Loaded customer support Q&A dataset from Hugging Face: `MohammadOthman/mo-customer-support-tweets-945k`
   - Cleaned null and duplicate values.
   - Saved as `clean_data.csv`.

2. **Embedding & Indexing:**
   - Used SentenceTransformer model `all-MiniLM-L6-v2` for embedding queries.
   - Built a FAISS vector index to support fast semantic similarity search.

3. **RAG Pipeline:**
   - **Retrieval:** Given a query, retrieve top 3 most semantically similar past Q&As.
   - **Augmentation:** Create a prompt by combining retrieved Q&As with the user's query.
   - **Generation:** Send the prompt to Falcon-7B via Hugging Face API to generate a final response.

4. **Serving via API:**
   - Used FastAPI to expose a `/generate` endpoint for the assistant.

---

## 🔄 RAG Implementation
**Retrieval**:
- Vector representation of queries built using `all-MiniLM-L6-v2`.
- Indexed using FAISS with L2 similarity.
- Search function retrieves top_k matches.

**Augmentation**:
- Selected top 3 matches.
- Created structured prompt with context Q&A + user query.

**Generation**:
- Used `tiiuae/falcon-7b-instruct` via Hugging Face Inference API.
- Output is post-processed to return only the generated answer.

---

## 📢 Explainability Techniques
- Matching Q&A pairs and similarity scores are logged and can be optionally returned.
- Keeps responses traceable and easy to debug.
- (Optional future enhancement: use LIME/SHAP for deeper model transparency.)

---

## 📦 Directory Structure
```
customer-support-ai/
├── app.py                            # FastAPI app entrypoint
├── pipeline.py                       # RAG pipeline (retriever + generator)
├── requirements.txt                  # Dependencies
├── README.md                         # Project overview & how to run
├── .gitignore                        # Ignore unwanted files (e.g., __pycache__)
│
├── rag/                              # Core logic of RAG
│   ├── __init__.py
│   ├── embedder.py                   # SentenceTransformer embedder
│   ├── vector_store.py               # FAISS vector DB logic
│   ├── retriever.py                  # Retrieval logic
│   ├── generator.py                  # LLM-based response generator
│
├── test/                             # Test scripts for each module
│   ├── __init__.py
│   ├── test_embedder.py              # (optional, can test embeddings)
│   ├── test_vector_store.py
│   ├── test_retriever.py
│   ├── test_generator.py
│   ├── test_pipeline.py
│
├── dataset/                          # Dataset preprocessing & raw/clean files
│   ├── dataset_preprocessor.py
│   ├── raw/                          # (optional) raw downloaded files
│   └── storage/                      # Cleaned CSV, FAISS index, mapping.pkl
│       ├── clean_data.csv
│       ├── faiss_index.index
│       ├── mapping.pkl
│
├── logs/                             # Logs for interaction history
│   └── conversations.csv


```

---

## 🚀 How to Run Locally
```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run FastAPI server
uvicorn app.main:app --reload
```

---

## 🔐 Notes on Security
- API key is stored in `.env` file and not pushed to GitHub.
- Use `python-dotenv` to load it securely.

---

## 🤝 Credits
Built by Aadil Maqbool for the Customer Support AI Assistant Challenge.

