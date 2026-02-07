import json
from typing import Optional, Dict, Any
from .llm_client import LLMClient


class ApplicationAgent:
    """Agent that uses a local TensorFlow model to answer application questions."""

    def __init__(self, profile: Dict[str, Any]):
        self.profile = profile
        self.llm = LLMClient(provider="tensorflow")

    async def answer_question(self, question: str) -> Dict[str, Any]:
        """Return a dict with an `answer` key using the local model."""
        
        resp = await self.llm.generate(profile=self.profile, question=question)

        # Normalize response into a consistent dict
        result: Dict[str, Any] = {
            "answer": resp.get("answer"),
            "confidence": resp.get("score") or resp.get("confidence"),
            "evidence": resp.get("evidence"),
        }

        return result