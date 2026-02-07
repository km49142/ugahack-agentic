import os
import asyncio
import json
from typing import Optional, Dict, Any

try:
    import tensorflow as tf
    import tensorflow_hub as hub
except ImportError:
    tf = None
    hub = None


class TensorFlowClient:
    """Local question-answering client using TensorFlow Hub."""

    def __init__(self):
        if not tf or not hub:
            raise RuntimeError("TensorFlow dependencies are not installed. Please pip install tensorflow tensorflow_hub.")
        
        # Load the Universal Sentence Encoder QA model
        print("📥 Loading TensorFlow QA model (this may take a moment on first run)...")
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-qa/3")
        print("✅ TensorFlow model loaded.")

    async def generate(self, profile: Dict[str, Any], question: str, **kwargs) -> dict:
        """
        Answers a question based on the provided profile using a local USE-QA model.
        """
        context = json.dumps(profile)
        
        # Run model inference
        def _inference():
            inputs = {
                "question": tf.constant([question]),
                "context": tf.constant([context])
            }
            return self.model(inputs)

        loop = asyncio.get_event_loop()
        outputs = await loop.run_in_executor(None, _inference)
        
        answer = outputs["answer"][0].numpy().decode("utf-8")

        if not answer:
            answer = f"Could not find an answer in the context for question: {question}"

        return {"answer": answer}


class LLMClient:
    """Factory for LLM clients (Optimized for TensorFlow)."""

    def __new__(cls, provider: str = "tensorflow") -> Any:
        if provider == "tensorflow":
            if not tf:
                raise ImportError("TensorFlow provider selected, but 'tensorflow' package is not installed.")
            return TensorFlowClient()
        else:
            raise ValueError(f"Provider '{provider}' is not supported. This build is optimized for TensorFlow only.")