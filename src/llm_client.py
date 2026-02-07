import os
import asyncio
import json
import re
from typing import Optional, Dict, Any

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import tensorflow as tf
    import tensorflow_hub as hub
except ImportError:
    tf = None
    hub = None


class AnthropicClient:
    """Simple Anthropic client wrapper."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if anthropic:
            try:
                self.client = anthropic.Client(api_key=self.api_key)
            except Exception:
                self.client = None
        else:
            self.client = None

    async def generate(self, prompt: str, max_tokens: int = 512) -> dict:
        """Generate text using Anthropic."""
        if not anthropic or not self.client:
            raise RuntimeError("anthropic package is not installed or client failed to initialize.")

        def _call():
            raw_prompt = prompt
            try:
                resp = self.client.completions.create(
                    model="claude-2",
                    prompt=(f"{anthropic.HUMAN_PROMPT} {raw_prompt} {anthropic.AI_PROMPT}"),
                    max_tokens_to_sample=max_tokens,
                )
                return resp.completion if hasattr(resp, 'completion') else str(resp)
            except Exception as e:
                return str(e)

        loop = asyncio.get_event_loop()
        text_response = await loop.run_in_executor(None, _call)

        try:
            return json.loads(text_response)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text_response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
        return {"text": text_response}


class TensorFlowClient:
    """Local question-answering client using TensorFlow Hub."""

    def __init__(self):
        if not tf or not hub:
            raise RuntimeError("TensorFlow dependencies are not installed. Please pip install tensorflow tensorflow_hub.")
        
        # Load the Universal Sentence Encoder QA model
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-qa/3")

    async def generate(self, profile: Dict[str, Any], question: str, **kwargs) -> dict:
        """
        Answers a question based on the provided profile using a local USE-QA model.
        """
        context = json.dumps(profile)
        
        # Run model inference
        inputs = {
            "question": tf.constant([question]),
            "context": tf.constant([context])
        }
        outputs = self.model(inputs)
        
        answer = outputs["answer"][0].numpy().decode("utf-8")

        if not answer:
            answer = f"Could not find an answer in the context for question: {question}"

        return {"answer": answer}


class LLMClient:
    """Factory for LLM clients."""

    def __new__(cls, provider: str = "anthropic", api_key: str | None = None) -> Any:
        if provider == "anthropic":
            if not anthropic:
                raise ImportError("Anthropic provider selected, but 'anthropic' package is not installed.")
            return AnthropicClient(api_key=api_key)
        elif provider == "tensorflow":
            if not tf:
                raise ImportError("TensorFlow provider selected, but 'tensorflow' package is not installed.")
            return TensorFlowClient()
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

