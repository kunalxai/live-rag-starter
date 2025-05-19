from fastapi import FastAPI
from .models import search

app = FastAPI()

@app.get("/query")
def query(q: str):
    results = search(q)
    return {"query": q, "results": results}
