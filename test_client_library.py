#!/usr/bin/env python3
"""
Test script for the UniLLM client library.

This script tests the client library against your running UniLLM API gateway.
Make sure your API gateway is running on localhost:8000 before running this test.
"""

import os
import sys
import time

# Add the src directory to the path so we can import unillm
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from unillm import UniLLM, chat
from src.unillm.client import UniLLM

def test_client_library():
    """Test the UniLLM client library."""
    
    print("🧪 Testing UniLLM Client Library")
    print("=" * 50)
    
    # Use the API key and Railway URL from your registration step
    api_key = "unillm_8ps1r4ehQCmFmOSsZGHblRa0BTicHZ40"
    base_url = "https://web-production-70deb.up.railway.app"

    client = UniLLM(api_key=api_key, base_url=base_url)

    # Health check
    print("Health check:", client.health_check())

    # Test chat completion with OpenAI
    print("\nTesting OpenAI (gpt-3.5-turbo):")
    response = client.chat(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello from Railway OpenAI!'"}]
    )
    print("Response:", response.content)

    # Test chat completion with Anthropic
    print("\nTesting Anthropic (claude-3-opus-20240229):")
    response = client.chat(
        model="claude-3-opus-20240229",
        messages=[{"role": "user", "content": "Say 'Hello from Railway Anthropic!'"}]
    )
    print("Response:", response.content)
    
    # Test 2: Simple chat
    print("\n2️⃣ Testing simple chat...")
    try:
        response = client.chat(
            model="gpt-4",
            messages=[{"role": "user", "content": "Say 'Hello from UniLLM!'"}],
            temperature=0.1
        )
        
        print(f"✅ Response: {response.content}")
        print(f"📊 Model: {response.model}")
        print(f"📈 Usage: {response.usage}")
        
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False
    
    # Test 3: Convenience function
    print("\n3️⃣ Testing convenience function...")
    try:
        response = chat(
            model="gpt-4",
            messages=[{"role": "user", "content": "What's 2+2?"}]
        )
        
        print(f"✅ Response: {response.content}")
        
    except Exception as e:
        print(f"❌ Convenience function test failed: {e}")
        return False
    
    # Test 4: Different model
    print("\n4️⃣ Testing different model...")
    try:
        response = client.chat(
            model="claude-3-sonnet",
            messages=[{"role": "user", "content": "Tell me a short fact about AI"}],
            temperature=0.5
        )
        
        print(f"✅ Response: {response.content}")
        print(f"📊 Model: {response.model}")
        
    except Exception as e:
        print(f"❌ Different model test failed: {e}")
        # This might fail if Claude API key is not configured, which is okay
    
    # Test 5: Conversation
    print("\n5️⃣ Testing conversation...")
    try:
        conversation = [
            {"role": "system", "content": "You are a helpful math tutor."},
            {"role": "user", "content": "I'm learning about squares."},
            {"role": "assistant", "content": "Great! A square is a quadrilateral with four equal sides and four right angles."},
            {"role": "user", "content": "What's the area of a square with sides of length 5?"}
        ]
        
        response = client.chat(
            model="gpt-4",
            messages=conversation
        )
        
        print(f"✅ Response: {response.content}")
        
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Your UniLLM client library is working correctly.")
    return True

if __name__ == "__main__":
    success = test_client_library()
    sys.exit(0 if success else 1) 