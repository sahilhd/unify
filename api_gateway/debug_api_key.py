#!/usr/bin/env python3
"""
Debug script to test API key validation
"""

import requests
import json

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@unillm.com"
TEST_PASSWORD = "testpassword123"

def debug_api_key():
    print("🔍 Debugging API Key Validation")
    print("=" * 50)
    
    # Step 1: Login to get user info
    print("1. Logging in...")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        login_info = response.json()
        jwt_token = login_info["access_token"]
        api_key = login_info["user"]["api_key"]
        print(f"✅ Login successful")
        print(f"   API Key: {api_key}")
        print(f"   JWT Token: {jwt_token[:20]}...")
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return
    
    # Step 2: Get user info with JWT
    print("\n2. Getting user info with JWT...")
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ User info retrieved")
        print(f"   Email: {user_info['email']}")
        print(f"   API Key: {user_info['api_key']}")
        print(f"   Credits: {user_info['credits']}")
        
        # Check if API keys match
        if user_info['api_key'] == api_key:
            print("✅ API keys match")
        else:
            print("❌ API keys don't match!")
            print(f"   Login API key: {api_key}")
            print(f"   User info API key: {user_info['api_key']}")
    else:
        print(f"❌ Get user info failed: {response.status_code} - {response.text}")
        return
    
    # Step 3: Test chat with API key
    print("\n3. Testing chat with API key...")
    chat_headers = {"Authorization": f"Bearer {api_key}"}
    chat_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello! What is 2+2?"}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(f"{BASE_URL}/chat/completions", json=chat_data, headers=chat_headers)
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 200:
        print("✅ Chat request successful!")
    else:
        print(f"❌ Chat request failed: {response.status_code}")
    
    # Step 4: Test with different header format
    print("\n4. Testing with different header format...")
    chat_headers2 = {"X-API-Key": api_key}
    response2 = requests.post(f"{BASE_URL}/chat/completions", json=chat_data, headers=chat_headers2)
    print(f"Response status (X-API-Key): {response2.status_code}")
    print(f"Response body (X-API-Key): {response2.text}")

if __name__ == "__main__":
    debug_api_key() 