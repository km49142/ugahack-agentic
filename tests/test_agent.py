import asyncio
import pytest

from src import llm_client
from src.agent import ApplicationAgent


@pytest.mark.asyncio
async def test_agent_parses_structured_response(monkeypatch):
    async def mock_generate(self, prompt: str, max_tokens: int = 512):
        return {
            "answer": "I have full work authorization.",
            "confidence": 0.95,
            "evidence": ["profile.personal_info.email: test@example.com"]
        }

    monkeypatch.setattr(llm_client.LLMClient, "generate", mock_generate)

    profile = {"personal_info": {"email": "test@example.com"}}
    agent = ApplicationAgent(profile)
    resp = await agent.answer_question("Are you authorized to work in the US?")

    assert isinstance(resp, dict)
    assert resp["answer"] == "I have full work authorization."
    assert isinstance(resp["confidence"], float)
    assert resp["confidence"] == pytest.approx(0.95)
    assert isinstance(resp["evidence"], list)


@pytest.mark.asyncio
async def test_agent_handles_text_response(monkeypatch):
    async def mock_generate(self, prompt: str, max_tokens: int = 512):
        return "Yes, I am willing to relocate."

    monkeypatch.setattr(llm_client.LLMClient, "generate", mock_generate)

    profile = {"personal_info": {"first_name": "Test"}}
    agent = ApplicationAgent(profile)
    resp = await agent.answer_question("Are you willing to relocate?")

    assert isinstance(resp, dict)
    assert resp["answer"] == "Yes, I am willing to relocate."
    assert resp["confidence"] is None
    assert resp["evidence"] is None
