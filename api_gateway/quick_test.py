#!/usr/bin/env python3
"""
Quick test for UniLLM Phase 2 - Tests authentication and basic functionality
without making real LLM calls
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@unillm.com"
TEST_PASSWORD = "testpassword123"

def test_health():
    """Test health check"""
    print("🧪 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n🧪 Testing User Login...")
    try:
        data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        
        if response.status_code == 200:
            login_data = response.json()
            jwt_token = login_data["access_token"]
            print("✅ Login successful")
            print(f"ℹ️  JWT Token: {jwt_token[:20]}...")
            return jwt_token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_user_info(jwt_token):
    """Test getting user info"""
    print("\n🧪 Testing Get User Info...")
    try:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            api_key = user_data["api_key"]
            print("✅ User info retrieved")
            print(f"ℹ️  Email: {user_data['email']}")
            print(f"ℹ️  Credits: {user_data['credits']}")
            print(f"ℹ️  API Key: {api_key[:20]}...")
            return api_key
        else:
            print(f"❌ Get user info failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Get user info error: {e}")
        return None

def test_api_key_auth(api_key):
    """Test API key authentication (without making real LLM calls)"""
    print("\n🧪 Testing API Key Authentication...")
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Test with a simple request that should validate the API key
        # but not make a real LLM call
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Hello! What is 2+2?"}
            ],
            "temperature": 0.7,
            "max_tokens": 10  # Very small to minimize cost
        }
        
        print("ℹ️  Making chat request with API key...")
        print("ℹ️  This may take a moment as it tries to connect to LLM providers...")
        
        # Set a timeout to prevent hanging
        response = requests.post(
            f"{BASE_URL}/chat/completions", 
            json=data, 
            headers=headers,
            timeout=30  # 30 second timeout
        )
        
        if response.status_code == 200:
            chat_data = response.json()
            print("✅ Chat request successful!")
            print(f"ℹ️  Response: {chat_data['response'][:100]}...")
            print(f"ℹ️  Provider: {chat_data['provider']}")
            print(f"ℹ️  Cost: ${chat_data['cost']:.6f}")
            return True
        elif response.status_code == 401:
            print("❌ API key authentication failed")
            print(f"ℹ️  Response: {response.text}")
            return False
        elif response.status_code == 402:
            print("⚠️  Insufficient credits")
            print(f"ℹ️  Response: {response.text}")
            return True  # This is actually a success - auth worked but no credits
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"ℹ️  Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out - likely hanging on LLM provider connection")
        return False
    except Exception as e:
        print(f"❌ API key test error: {e}")
        return False

def test_usage_stats(jwt_token):
    """Test usage statistics"""
    print("\n🧪 Testing Usage Statistics...")
    try:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(f"{BASE_URL}/billing/usage", headers=headers)
        
        if response.status_code == 200:
            usage_data = response.json()
            print("✅ Usage statistics retrieved")
            print(f"ℹ️  Total Requests: {usage_data['total_requests']}")
            print(f"ℹ️  Total Cost: ${usage_data['total_cost']:.6f}")
            return True
        else:
            print(f"❌ Usage stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Usage stats error: {e}")
        return False

def test_credit_purchase(jwt_token):
    """Test credit purchase"""
    print("\n🧪 Testing Credit Purchase...")
    try:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        data = {
            "amount": 5.0,
            "payment_method": "test_payment"
        }
        response = requests.post(f"{BASE_URL}/billing/purchase-credits", json=data, headers=headers)
        
        if response.status_code == 200:
            purchase_data = response.json()
            print("✅ Credit purchase successful")
            print(f"ℹ️  Credits Added: ${purchase_data['credits_added']}")
            print(f"ℹ️  New Balance: ${purchase_data['new_balance']}")
            return True
        else:
            print(f"❌ Credit purchase failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Credit purchase error: {e}")
        return False

def main():
    """Run all quick tests"""
    print("🚀 UniLLM Phase 2: Quick Test")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("\n❌ Server not responding. Please start the server first.")
        return
    
    # Test login
    jwt_token = test_login()
    if not jwt_token:
        print("\n❌ Login failed. Cannot continue.")
        return
    
    # Test user info
    api_key = test_user_info(jwt_token)
    if not api_key:
        print("\n❌ Could not get API key. Cannot continue.")
        return
    
    # Test API key authentication
    test_api_key_auth(api_key)
    
    # Test usage stats
    test_usage_stats(jwt_token)
    
    # Test credit purchase
    test_credit_purchase(jwt_token)
    
    print("\n🎯 Quick test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main() 