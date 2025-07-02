#!/usr/bin/env python3
"""
Simple API Test for UniLLM
Tests core functionality without streaming
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test_{int(time.time())}@example.com"
TEST_PASSWORD = "testpass123"

def print_step(step, description):
    print(f"\n{'='*50}")
    print(f"STEP {step}: {description}")
    print(f"{'='*50}")

def test_health():
    """Test health endpoint"""
    print_step(1, "Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_register():
    """Test user registration"""
    print_step(2, "Testing User Registration")
    try:
        data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Registration successful")
            print(f"   Email: {user_data.get('email')}")
            print(f"   API Key: {user_data.get('api_key')[:20]}...")
            return user_data.get('api_key')
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_login():
    """Test user login"""
    print_step(3, "Testing User Login")
    try:
        data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        if response.status_code == 200:
            login_data = response.json()
            print(f"✅ Login successful")
            print(f"   Access Token: {login_data.get('access_token')[:20]}...")
            return login_data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_user_info(api_key):
    """Test getting user info"""
    print_step(4, "Testing User Info")
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User info retrieved")
            print(f"   Email: {user_data.get('email')}")
            print(f"   Credits: ${user_data.get('credits')}")
            print(f"   Rate Limit: {user_data.get('rate_limit_per_minute')}/min")
            return True
        else:
            print(f"❌ User info failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ User info error: {e}")
        return False

def test_chat_completion(api_key, model="gpt-3.5-turbo"):
    """Test chat completion"""
    print_step(5, f"Testing Chat Completion with {model}")
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Say 'Hello from UniLLM!'"}
            ],
            "temperature": 0.7,
            "max_tokens": 50,
            "stream": False  # Explicitly set to False
        }
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
        if response.status_code == 200:
            chat_data = response.json()
            print(f"✅ Chat completion successful")
            print(f"   Response: {chat_data.get('response')}")
            print(f"   Provider: {chat_data.get('provider')}")
            print(f"   Tokens: {chat_data.get('tokens')}")
            print(f"   Cost: ${chat_data.get('cost')}")
            print(f"   Remaining Credits: ${chat_data.get('remaining_credits')}")
            return True
        else:
            print(f"❌ Chat completion failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat completion error: {e}")
        return False

def test_anthropic_chat(api_key):
    """Test Anthropic chat completion"""
    print_step(6, "Testing Anthropic Chat Completion")
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {
            "model": "claude-3-sonnet-20240229",
            "messages": [
                {"role": "user", "content": "Say 'Hello from Anthropic!'"}
            ],
            "temperature": 0.7,
            "max_tokens": 50,
            "stream": False
        }
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
        if response.status_code == 200:
            chat_data = response.json()
            print(f"✅ Anthropic chat completion successful")
            print(f"   Response: {chat_data.get('response')}")
            print(f"   Provider: {chat_data.get('provider')}")
            return True
        else:
            print(f"❌ Anthropic chat completion failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Anthropic chat completion error: {e}")
        return False

def test_usage_stats(api_key):
    """Test usage statistics"""
    print_step(7, "Testing Usage Statistics")
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{BASE_URL}/billing/usage", headers=headers)
        if response.status_code == 200:
            usage_data = response.json()
            print(f"✅ Usage stats retrieved")
            print(f"   Total Requests: {usage_data.get('total_requests')}")
            print(f"   Total Tokens: {usage_data.get('total_tokens')}")
            print(f"   Total Cost: ${usage_data.get('total_cost')}")
            print(f"   Requests Today: {usage_data.get('requests_today')}")
            return True
        else:
            print(f"❌ Usage stats failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Usage stats error: {e}")
        return False

def test_models():
    """Test models endpoint"""
    print_step(8, "Testing Models Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/models")
        if response.status_code == 200:
            models_data = response.json()
            print(f"✅ Models retrieved")
            print(f"   Available Models: {len(models_data)}")
            for model in models_data[:5]:  # Show first 5 models
                print(f"   - {model.get('id')} ({model.get('provider')})")
            return True
        else:
            print(f"❌ Models failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Models error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 UniLLM API Test Suite")
    print("Testing core functionality without streaming")
    
    # Test health first
    if not test_health():
        print("\n❌ Health check failed. Is the server running?")
        return
    
    # Test registration
    api_key = test_register()
    if not api_key:
        print("\n❌ Registration failed. Cannot continue.")
        return
    
    # Test login
    jwt_token = test_login()
    if not jwt_token:
        print("\n❌ Login failed. Cannot continue.")
        return
    
    # Test user info
    if not test_user_info(api_key):
        print("\n❌ User info failed.")
        return
    
    # Test OpenAI chat
    if not test_chat_completion(api_key, "gpt-3.5-turbo"):
        print("\n❌ OpenAI chat failed.")
        return
    
    # Test Anthropic chat
    if not test_anthropic_chat(api_key):
        print("\n❌ Anthropic chat failed.")
        return
    
    # Test usage stats
    if not test_usage_stats(api_key):
        print("\n❌ Usage stats failed.")
        return
    
    # Test models
    if not test_models():
        print("\n❌ Models endpoint failed.")
        return
    
    print(f"\n{'='*50}")
    print("🎉 ALL TESTS PASSED!")
    print("✅ Core API functionality is working correctly")
    print("✅ Ready for frontend deployment")
    print(f"{'='*50}")

if __name__ == "__main__":
    main() 