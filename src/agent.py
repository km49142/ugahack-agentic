import json
from typing import Optional, Dict, Any
from .llm_client import LLMClient


PROMPT_TEMPLATE = (
    "You are an assistant that helps fill job application questions.\n"
    "Return a JSON object with an `answer` field. Be concise and do not invent facts.\n\n"
    "Profile (JSON):\n{profile}\n\n"
    "Question:\n{question}\n\n"
    "Return only JSON."
)


class ApplicationAgent:
    """Agent that uses an LLM to answer open-ended application questions."""

    def __init__(self, profile: Dict[str, Any], provider: str = "anthropic"):
        self.profile = profile
        self.provider = provider
        self.llm = LLMClient(provider=provider)

    async def answer_question(self, question: str, schema: Optional[Dict] = None) -> Dict[str, Any]:
        """Return a dict with at minimum an `answer` key.

        The `schema` argument is currently advisory; the LLM will be prompted
        to return JSON with an `answer` key.
        """
        if self.provider == "tensorflow":
            resp = await self.llm.generate(profile=self.profile, question=question)
        else:
            prompt = PROMPT_TEMPLATE.format(profile=json.dumps(self.profile, indent=2), question=question)
            resp = await self.llm.generate(prompt)

        # Normalize different response shapes into a consistent dict
        result: Dict[str, Any] = {
            "answer": None,
            "confidence": None,
            "evidence": None,
        }

        # If LLM returned a dict-like structured response
        if isinstance(resp, dict):
            # direct answer
            if "answer" in resp:
                result["answer"] = resp.get("answer")
            # fallback to common keys
            elif "text" in resp:
                result["answer"] = resp.get("text")
            else:
                # if entire dict looks like a raw string map, stringify
                result["answer"] = str(resp)

            # confidence may be present as number or string
            conf = resp.get("confidence") or resp.get("score") or resp.get("probability")
            if conf is not None:
                try:
                    result["confidence"] = float(conf)
                except Exception:
                    # try to extract number from string
                    try:
                        import re

                        m = re.search(r"\d+\.?\d*", str(conf))
                        if m:
                            result["confidence"] = float(m.group(0))
                    except Exception:
                        result["confidence"] = None

            # evidence can be string or list
            ev = resp.get("evidence") or resp.get("sources")
            if ev is not None:
                result["evidence"] = ev

            return result

        # If LLM returned raw string, place into answer
        result["answer"] = str(resp)
        return result
