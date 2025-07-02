#!/usr/bin/env python3
"""
Test script to register a new user on the deployed backend
and get a fresh API key for testing
"""

import requests
import time

API_URL = "https://web-production-70deb.up.railway.app"
EMAIL = f"test_{int(time.time())}@example.com"
PASSWORD = "testpass123"

def test_deployed_backend():
    print("🔍 Testing deployed backend...")
    
    # Step 1: Test health endpoint
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json().get('status')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Step 2: Register new user
    print("\n2️⃣ Registering new user...")
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": EMAIL,
                "password": PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            api_key = data.get("api_key")
            print("✅ Registration successful")
            print(f"   Email: {EMAIL}")
            print(f"   API Key: {api_key}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 3: Test API key with chat
    print("\n3️⃣ Testing API key with chat...")
    try:
        response = requests.post(
            f"{API_URL}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hello from deployed backend!"}],
                "temperature": 0.7,
                "max_tokens": 50
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat request successful")
            print(f"   Response: {data.get('choices', [{}])[0].get('message', {}).get('content', 'No content')}")
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Chat request error: {e}")
        return
    
    # Step 4: Test Anthropic model
    print("\n4️⃣ Testing Anthropic model...")
    try:
        response = requests.post(
            f"{API_URL}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "claude-3-sonnet-20240229",
                "messages": [{"role": "user", "content": "Say 'Hello from Claude!'"}],
                "temperature": 0.7,
                "max_tokens": 30
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Anthropic request successful")
            print(f"   Response: {data.get('choices', [{}])[0].get('message', {}).get('content', 'No content')}")
        else:
            print(f"❌ Anthropic request failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Anthropic request error: {e}")
    
    print(f"\n🎉 Test completed! Use this API key for your friend's computer:")
    print(f"API_KEY = \"{api_key}\"")

if __name__ == "__main__":
    test_deployed_backend() 