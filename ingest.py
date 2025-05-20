from fastapi import APIRouter, UploadFile, File, HTTPException
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import numpy as np
import faiss
import os

router = APIRouter()

# Globals (simulate shared memory)
model = SentenceTransformer("all-MiniLM-L6-v2")
index_file = "index.faiss"
doc_store = []
next_id = 0

# Load or initialize FAISS index
if os.path.exists(index_file):
    index = faiss.read_index(index_file)
else:
    index = faiss.IndexIDMap(faiss.IndexFlatL2(384))  # ID-mapped

def extract_text(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        return " ".join([page.extract_text() for page in reader.pages])
    elif file.filename.endswith(".txt"):
        return file.file.read().decode()
    else:
        raise HTTPException(400, "Unsupported file type")

def chunk_text(text: str, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    global next_id, doc_store
    text = extract_text(file)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)
    ids = list(range(next_id, next_id + len(chunks)))

    index.add_with_ids(np.array(embeddings), np.array(ids))
    doc_store.extend(chunks)
    next_id += len(chunks)
    faiss.write_index(index, index_file)
    return {"message": f"Ingested {len(chunks)} chunks"}
