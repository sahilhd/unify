#!/usr/bin/env python3
"""
Simple chat test for Phase 2
"""

import requests
import time

# Test configuration
BASE_URL = "http://localhost:8000"

# Test user credentials
test_email = f"test_{int(time.time())}@example.com"
test_password = "testpass123"

print(f"🚀 Simple Chat Test with email {test_email}")
print("=" * 50)

# Step 1: Register user
print("\n1️⃣ Registering user...")
try:
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": test_email, "password": test_password},
        timeout=10
    )
    if response.status_code == 200:
        user_data = response.json()
        api_key = user_data["api_key"]
        print(f"✅ Registered: {user_data['email']}")
        print(f"   API Key: {api_key[:20]}...")
    else:
        print(f"❌ Registration failed: {response.status_code} - {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ Registration error: {e}")
    exit(1)

# Step 2: Test chat with API key
print("\n2️⃣ Testing chat with API key...")
try:
    chat_response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say hello in one word"}],
            "max_tokens": 10
        },
        timeout=60  # Longer timeout for LLM call
    )
    
    print(f"   Status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        result = chat_response.json()
        print(f"✅ Chat successful!")
        print(f"   Response: {result.get('response', 'No response')}")
        print(f"   Provider: {result.get('provider', 'Unknown')}")
        print(f"   Cost: {result.get('cost', 0)}")
        print(f"   Remaining credits: {result.get('remaining_credits', 0)}")
    else:
        print(f"❌ Chat failed: {chat_response.text}")
        
except Exception as e:
    print(f"❌ Chat error: {e}")

print("\n🎉 Simple chat test completed!") 