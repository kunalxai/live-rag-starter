from fastapi import FastAPI
from .models import search
from ingest import router as ingest_router
from prep_meeting import router as prep_router

app = FastAPI()

app.include_router(ingest_router)
app.include_router(prep_router)

@app.get("/query")
def query(q: str):
    results = search(q)
    return {"query": q, "results": results}
