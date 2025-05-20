from fastapi import APIRouter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

router = APIRouter()

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("index.faiss")
doc_store = []  # Will be updated in memory

def get_event_keywords(title: str, date: str):
    return title.split() + [date]

@router.get("/prep-meeting")
async def prep_meeting(title: str, date: str):
    query = " ".join(get_event_keywords(title, date))
    query_embed = model.encode([query])
    _, indices = index.search(np.array(query_embed), 5)

    summaries = []
    for i in indices[0]:
        if 0 <= i < len(doc_store):
            summaries.append(doc_store[i][:200])
    return {"title": title, "date": date, "summaries": summaries}
