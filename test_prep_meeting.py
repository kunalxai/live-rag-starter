import requests

BASE_URL = "http://localhost:8000"

def test_prep_meeting():
    params = {"title": "Annual Review", "date": "2025-05-20"}
    response = requests.get(f"{BASE_URL}/prep-meeting", params=params)

    assert response.status_code == 200
    data = response.json()
    assert "title" in data and "date" in data and "summaries" in data
    assert isinstance(data["summaries"], list)

    print("📋 Prep Meeting Response:")
    for s in data["summaries"]:
        print("-", s)
        assert len(s) <= 200, "Summary exceeds 200 characters"

if __name__ == "__main__":
    test_prep_meeting()
