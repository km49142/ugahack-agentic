import asyncio
import json
import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Monkeypatch the LLM client classes
from src import llm_client as llm_mod

async def mock_generate(self, *args, **kwargs):
    return {"answer": "Yes, I am willing to relocate.", "score": 0.99}

# Mock model loading to avoid downloading
def mock_init(self):
    print("[MOCK] TensorFlow model initialized.")

llm_mod.TensorFlowClient.__init__ = mock_init
llm_mod.TensorFlowClient.generate = mock_generate

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

    print("🤖 Starting Agent Smoke Test (TensorFlow Only)...")
    agent = ApplicationAgent(profile)
    resp = await agent.answer_question("Are you willing to relocate?")
    print("Agent response:", json.dumps(resp, indent=2))
    
    assert resp["answer"] == "Yes, I am willing to relocate."
    print("\n✅ Smoke test passed!")

if __name__ == '__main__':
    asyncio.run(run_smoke())