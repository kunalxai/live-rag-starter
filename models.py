import faiss
import os

# load or build your FAISS index
index = faiss.read_index("index.faiss") if os.path.exists("index.faiss") else faiss.IndexFlatL2(768)

def search(query: str, k: int = 5):
    # dummy embedding for now
    vec = [0.0] * 768  
    D, I = index.search([vec], k)
    return [{"id": int(i), "dist": float(d)} for d, i in zip(D[0], I[0])]
