import os
import asyncio
import json
import numpy as np
from typing import Optional, Dict, Any, List

try:
    import tensorflow as tf
    import tensorflow_hub as hub
except ImportError:
    tf = None
    hub = None


class TensorFlowClient:
    """Local retrieval-based client using Universal Sentence Encoder."""

    def __init__(self):
        if not tf or not hub:
            raise RuntimeError("TensorFlow dependencies are not installed. Please pip install tensorflow tensorflow_hub.")
        
        print("📥 Loading Universal Sentence Encoder (v4)...")
        # Use the standard v4 model which is simpler and more robust for general embedding
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        print("✅ TensorFlow model loaded.")

    def _flatten_profile(self, profile: Dict[str, Any]) -> List[str]:
        """Convert nested profile dict into a list of 'key: value' fact strings."""
        facts = []
        
        def recurse(data, prefix=""):
            if isinstance(data, dict):
                for k, v in data.items():
                    # clean key
                    clean_k = k.replace('_', ' ')
                    new_prefix = f"{prefix} {clean_k}" if prefix else clean_k
                    recurse(v, new_prefix)
            elif isinstance(data, list):
                for item in data:
                    recurse(item, prefix)
            elif data is not None and str(data).strip():
                # It's a leaf value
                facts.append(f"{prefix}: {data}")
                
        recurse(profile)
        # Add some combined/synthetic facts for better matching
        p = profile.get('personal_info', {})
        if p:
            facts.append(f"My full name is {p.get('first_name', '')} {p.get('last_name', '')}")
            facts.append(f"I live in {p.get('address', {}).get('city', '')}, {p.get('address', {}).get('state', '')}")
            
        return facts

    async def generate(self, profile: Dict[str, Any], question: str, **kwargs) -> dict:
        """
        Finds the best matching fact from the profile for the given question.
        """
        # 1. Flatten profile into candidate answers
        candidates = self._flatten_profile(profile)
        if not candidates:
            return {"answer": "I don't have enough information in my profile."}

        # 2. Run inference in a separate thread (CPU bound)
        def _inference():
            # Embed the question
            # Embed all candidates
            all_text = [question] + candidates
            embeddings = self.model(all_text)
            
            # Calculate cosine similarity (dot product for normalized vectors)
            # USE vectors are approximately normalized, but let's be safe if we want strict cosine
            # The raw outputs of USE are already normalized to length 1 usually.
            
            q_vec = embeddings[0]
            cand_vecs = embeddings[1:]
            
            # Scores = dot product of q_vec with every cand_vec
            scores = tf.tensordot(cand_vecs, q_vec, axes=1)
            
            best_idx = tf.argmax(scores).numpy()
            best_score = scores[best_idx].numpy()
            
            return candidates[best_idx], float(best_score)

        loop = asyncio.get_event_loop()
        best_answer, score = await loop.run_in_executor(None, _inference)
        
        # Simple threshold
        if score < 0.2:
            return {
                "answer": f"I am not sure. (Best guess: {best_answer}, Confidence: {score:.2f})",
                "score": score,
                "evidence": [best_answer]
            }

        # Clean up the answer (remove the "key: " prefix if possible, or just return it)
        # For a form filler, returning the value part is often better, 
        # but the agent might be answering "Why..." questions.
        # Let's return the full fact for now, as it's safer context.
        
        # If the question asks "Why..." and we match a skill, we might want to frame it better.
        # But as a retrieval agent, returning the fact is the ground truth.
        
        return {
            "answer": best_answer,
            "score": score,
            "evidence": [best_answer]
        }


class LLMClient:
    """Factory for LLM clients (Optimized for TensorFlow)."""

    def __new__(cls, provider: str = "tensorflow") -> Any:
        if provider == "tensorflow":
            if not tf:
                raise ImportError("TensorFlow provider selected, but 'tensorflow' package is not installed.")
            return TensorFlowClient()
        else:
            raise ValueError(f"Provider '{provider}' is not supported. This build is optimized for TensorFlow only.")
