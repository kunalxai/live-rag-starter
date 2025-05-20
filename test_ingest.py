import requests
import time

BASE_URL = "http://localhost:8000"
SAMPLE_FILE = "sample_docs/sample.txt"
KEYWORD = "philosophy"

def query(keyword):
    response = requests.get(f"{BASE_URL}/query", params={"q": keyword})
    return response.json().get("results", [])

def ingest():
    with open(SAMPLE_FILE, "rb") as f:
        response = requests.post(f"{BASE_URL}/ingest", files={"file": ("sample.txt", f)})
    return response.json()

def test_ingest_flow():
    print("🔍 Searching for keyword before ingestion...")
    before = query(KEYWORD)
    print("Results before ingest:", before)

    print("\n📥 Ingesting document...")
    result = ingest()
    print("Ingest response:", result)

if __name__ == "__main__":
    test_ingest_flow()
