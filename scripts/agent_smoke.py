import asyncio
import json
import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import ApplicationAgent

async def run_smoke():
    print("🤖 Initializing Real TensorFlow Agent...")
    
    profile = {
        "personal_info": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "bio": "I am passionate about building autonomous AI agents and have 3 years of experience with Python and TensorFlow."
        },
        "skills": {
            "technical": ["Python", "TensorFlow", "React"]
        }
    }

    try:
        agent = ApplicationAgent(profile)
        
        print("\n❓ Question: Why are you passionate about AI?")
        resp = await agent.answer_question("Why are you passionate about AI?")
        print(f"💡 Answer: {resp['answer']}")
        print(f"   (Score: {resp.get('confidence', 0):.4f})")
        
        print("\n❓ Question: What is your email?")
        resp = await agent.answer_question("What is your email address?")
        print(f"💡 Answer: {resp['answer']}")
        
        print("\n✅ Smoke test complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(run_smoke())
