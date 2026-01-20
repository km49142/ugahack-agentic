import asyncio
import json
import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Monkeypatch the LLM client to avoid network calls
from src import llm_client as llm_mod

async def mock_generate(self, prompt: str, max_tokens: int = 512):
    # Simple mock that returns a JSON-like dict
    return {"answer": "Yes, I am willing to relocate."}

llm_mod.LLMClient.generate = mock_generate

from src.agent import ApplicationAgent

async def run_smoke():
    profile = {
        "personal_info": {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        },
        "education": [],
        "documents": {}
    }

    agent = ApplicationAgent(profile, provider="anthropic")
    resp = await agent.answer_question("Are you willing to relocate?")
    print("Agent response:", json.dumps(resp, indent=2))

if __name__ == '__main__':
    asyncio.run(run_smoke())
