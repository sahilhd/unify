#!/usr/bin/env python3
"""
Test script for Phase 1 API Gateway authentication
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found in environment")
    exit(1)

print(f"🔑 Using API key: {api_key[:10]}...")

# Test the Phase 1 server
base_url = "http://localhost:8000"

# Test 1: Health check (no auth required)
print("\n1️⃣ Testing health check...")
try:
    response = requests.get(f"{base_url}/health", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Health check passed")
    else:
        print(f"   ❌ Health check failed: {response.text}")
except Exception as e:
    print(f"   ❌ Health check error: {e}")

# Test 2: Models endpoint (no auth required)
print("\n2️⃣ Testing models endpoint...")
try:
    response = requests.get(f"{base_url}/models", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Models endpoint passed")
        models = response.json()
        print(f"   Available models: {len(models)}")
    else:
        print(f"   ❌ Models endpoint failed: {response.text}")
except Exception as e:
    print(f"   ❌ Models endpoint error: {e}")

# Test 3: Chat completions with Bearer token
print("\n3️⃣ Testing chat completions with Bearer token...")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello! Say 'Hello from Phase 1!'"}
    ],
    "temperature": 0.7,
    "max_tokens": 50
}

try:
    response = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Chat completions passed")
        result = response.json()
        print(f"   Response: {result['content']}")
        print(f"   Provider: {result['provider']}")
        print(f"   Model: {result['model']}")
    else:
        print(f"   ❌ Chat completions failed: {response.text}")
except Exception as e:
    print(f"   ❌ Chat completions error: {e}")

# Test 4: Chat completions without Bearer token (should fail)
print("\n4️⃣ Testing chat completions without Bearer token...")
try:
    response = requests.post(
        f"{base_url}/chat/completions",
        json=payload,
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✅ Correctly rejected unauthorized request")
    else:
        print(f"   ❌ Unexpected response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n🎉 Phase 1 authentication test completed!") 