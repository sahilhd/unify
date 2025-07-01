#!/usr/bin/env python3
"""
Check environment variables for Phase 2
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Environment Variables Check")
print("=" * 40)

# Check OpenAI API key
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    print(f"✅ OPENAI_API_KEY: {openai_key[:10]}...")
    print(f"   Length: {len(openai_key)} characters")
    if openai_key.startswith("sk-"):
        print("   ✅ Valid format (starts with sk-)")
    else:
        print("   ⚠️  Unexpected format")
else:
    print("❌ OPENAI_API_KEY: Not found")

# Check other provider keys
providers = ["ANTHROPIC_API_KEY", "GEMINI_API_KEY", "MISTRAL_API_KEY", "COHERE_API_KEY"]
for provider in providers:
    key = os.getenv(provider)
    if key:
        print(f"✅ {provider}: {key[:10]}...")
    else:
        print(f"⚠️  {provider}: Not set (optional)")

# Check database URL
db_url = os.getenv("DATABASE_URL", "sqlite:///./unillm.db")
print(f"✅ DATABASE_URL: {db_url}")

# Check Redis URL
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
print(f"✅ REDIS_URL: {redis_url}")

print("\n📝 Summary:")
if openai_key:
    print("✅ OpenAI API key is set - Phase 2 should work")
else:
    print("❌ OpenAI API key is missing - Phase 2 will hang on LLM calls")

print("\n💡 If OpenAI key is missing, add it to your .env file:")
print("OPENAI_API_KEY=sk-proj-VD...") 