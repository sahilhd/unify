#!/usr/bin/env python3
"""
Simple test for PyPI version 0.1.4
"""

from unillm import UniLLM

# Initialize with explicit base URL for SaaS platform
client = UniLLM(
    api_key="unillm_yL5miUBRVH3qwVrMPCYfJ8u8dicMJ96x",
    base_url="https://web-production-70deb.up.railway.app"
)

print("🚀 Testing PyPI v0.1.4 with SaaS platform")
print("=" * 50)

# Test OpenAI
print("\n🧪 Testing GPT-4...")
try:
    response = client.chat(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
    )
    print(f"✅ GPT-4 working!")
    print(f"   Response: {response.content}")
except Exception as e:
    print(f"❌ GPT-4 failed: {e}")

# Test Anthropic
print("\n🧪 Testing Claude...")
try:
    response = client.chat(
        model="claude-3-sonnet",
        messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
    )
    print(f"✅ Claude working!")
    print(f"   Response: {response.content}")
except Exception as e:
    print(f"❌ Claude failed: {e}")

# Test Gemini
print("\n🧪 Testing Gemini...")
try:
    response = client.chat(
        model="gemini-1.5-flash",
        messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
    )
    print(f"✅ Gemini working!")
    print(f"   Response: {response.content}")
except Exception as e:
    print(f"❌ Gemini failed: {e}")

print("\n🎉 Test completed!") 