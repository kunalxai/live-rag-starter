from langchain.agents import tool, initialize_agent
from langchain.chat_models import ChatOpenAI
import requests
import os

@tool
def ingest_tool(file_path: str) -> str:
    """Uploads a file to the /ingest endpoint."""
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                "http://localhost:8000/ingest",
                files={"file": (os.path.basename(file_path), f)}
            )
            return response.json()["message"]
    except Exception as e:
        return f"Failed: {str(e)}"

@tool
def prep_tool(title_date: str) -> str:
    """Gets meeting summaries. Format: Title,YYYY-MM-DD"""
    try:
        title, date = title_date.split(",")
        response = requests.get("http://localhost:8000/prep-meeting", params={"title": title, "date": date})
        return str(response.json())
    except Exception as e:
        return f"Failed: {str(e)}"

llm = ChatOpenAI(temperature=0)
tools = [ingest_tool, prep_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

if __name__ == "__main__":
    print(agent.run("Add this doc: ./sample_docs/sample.pdf"))
    print(agent.run("What is discussed in: Team Sync,2025-05-15"))
