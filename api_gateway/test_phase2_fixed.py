#!/usr/bin/env python3
"""
Fixed Phase 2 test script with unique emails
"""

import requests
import time
import uuid
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"

# Generate unique test email
test_email = f"test_{int(time.time())}@example.com"
test_password = "testpass123"

print(f"🚀 UniLLM Phase 2: Testing with email {test_email}")
print("=" * 60)

# Test 1: Health Check
print("\n🧪 Health Check")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    if response.status_code == 200:
        print("✅ Health check passed")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Health check error: {e}")

# Test 2: User Registration
print("\n🧪 User Registration")
try:
    registration_data = {
        "email": test_email,
        "password": test_password
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=registration_data, timeout=10)
    
    if response.status_code == 200:
        print("✅ Registration successful")
        user_data = response.json()
        api_key = user_data.get("api_key", "N/A")
        credits = user_data.get("credits", 0)
        print(f"   API Key: {api_key[:20]}...")
        print(f"   Credits: {credits}")
    else:
        print(f"❌ Registration failed: {response.status_code} - {response.text}")
        api_key = None
except Exception as e:
    print(f"❌ Registration error: {e}")
    api_key = None

# Test 3: User Login
print("\n🧪 User Login")
try:
    login_data = {
        "email": test_email,
        "password": test_password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
    
    if response.status_code == 200:
        print("✅ Login successful")
        login_data = response.json()
        jwt_token = login_data.get("access_token", "N/A")
        print(f"   JWT Token: {jwt_token[:20]}...")
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        jwt_token = None
except Exception as e:
    print(f"❌ Login error: {e}")
    jwt_token = None

# Test 4: Get User Info
print("\n🧪 Get User Info")
if jwt_token:
    try:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ User info retrieved")
            user_info = response.json()
            print(f"   Email: {user_info.get('email')}")
            print(f"   Credits: {user_info.get('credits')}")
            print(f"   API Key: {user_info.get('api_key', 'N/A')[:20]}...")
        else:
            print(f"❌ User info failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ User info error: {e}")

# Test 5: Chat with API Key
print("\n🧪 Chat with API Key")
if api_key:
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        chat_data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Hello! Say 'Phase 2 is working!'"}
            ],
            "max_tokens": 50
        }
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=chat_data, timeout=30)
        
        if response.status_code == 200:
            print("✅ Chat successful")
            chat_response = response.json()
            print(f"   Response: {chat_response.get('response', 'N/A')}")
            print(f"   Provider: {chat_response.get('provider', 'N/A')}")
            print(f"   Cost: {chat_response.get('cost', 'N/A')}")
            print(f"   Remaining credits: {chat_response.get('remaining_credits', 'N/A')}")
        else:
            print(f"❌ Chat failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Chat error: {e}")

# Test 6: Usage Stats
print("\n🧪 Usage Stats")
try:
    response = requests.get(
        f"{BASE_URL}/billing/usage",
        headers={"Authorization": f"Bearer {jwt_token}"},
        timeout=10
    )
    if response.status_code == 200:
        print("✅ Usage stats retrieved")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Usage stats failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Usage stats error: {e}")

# Test 7: Purchase Credits
print("\n🧪 Purchase Credits")
try:
    response = requests.post(
        f"{BASE_URL}/billing/purchase-credits",
        headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"},
        json={"amount": 50.0, "payment_method": "test"},
        timeout=10
    )
    if response.status_code == 200:
        print("✅ Credits purchased")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Credit purchase failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Credit purchase error: {e}")

print("\n🎉 Phase 2 testing completed!")
print(f"📧 Test email used: {test_email}") 