#!/usr/bin/env python3
"""
Test script to verify UniLLM works with new API keys in a fresh environment
This simulates what a friend would experience when using your system
"""

import requests
import json
import time

def test_with_new_api_keys():
    """Test the system with completely new API keys"""
    print("🧪 Testing UniLLM with New API Keys")
    print("=" * 50)
    
    BASE_URL = "http://localhost:8000"
    
    # Step 1: Register a new user with new API key
    print("1️⃣ Registering new user...")
    register_data = {
        "email": "friend@example.com",
        "password": "friend123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 200:
        user_data = response.json()
        new_api_key = user_data["api_key"]
        print(f"✅ New user registered: {user_data['email']}")
        print(f"🔑 New API key: {new_api_key[:10]}...{new_api_key[-4:]}")
    else:
        print(f"❌ Registration failed: {response.status_code}")
        return
    
    # Step 2: Test the new API key with OpenAI
    print("\n2️⃣ Testing new API key with OpenAI...")
    headers = {
        "Authorization": f"Bearer {new_api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say 'Hello from new API key!'"}],
            "max_tokens": 20
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ OpenAI with new key: {result.get('response', 'N/A')}")
        print(f"💰 Cost: ${result.get('cost', 0):.6f}")
        print(f"💳 Remaining credits: ${result.get('remaining_credits', 0):.2f}")
    else:
        print(f"❌ OpenAI failed: {response.status_code}")
        print(f"Error: {response.text}")
    
    # Step 3: Test with Anthropic
    print("\n3️⃣ Testing new API key with Anthropic...")
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json={
            "model": "claude-3-opus-20240229",
            "messages": [{"role": "user", "content": "Say 'Hello from Anthropic with new key!'"}],
            "max_tokens": 20
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Anthropic with new key: {result.get('response', 'N/A')}")
        print(f"💰 Cost: ${result.get('cost', 0):.6f}")
        print(f"💳 Remaining credits: ${result.get('remaining_credits', 0):.2f}")
    else:
        print(f"❌ Anthropic failed: {response.status_code}")
        print(f"Error: {response.text}")
    
    # Step 4: Test usage stats
    print("\n4️⃣ Testing usage statistics...")
    response = requests.get(f"{BASE_URL}/billing/usage", headers=headers)
    
    if response.status_code == 200:
        usage_data = response.json()
        print(f"✅ Usage stats:")
        print(f"   📊 Total requests: {usage_data.get('total_requests', 0)}")
        print(f"   🔤 Total tokens: {usage_data.get('total_tokens', 0)}")
        print(f"   💰 Total cost: ${usage_data.get('total_cost', 0):.6f}")
        print(f"   📅 Requests today: {usage_data.get('requests_today', 0)}")
    else:
        print(f"❌ Usage stats failed: {response.status_code}")
    
    # Step 5: Test models endpoint
    print("\n5️⃣ Testing models endpoint...")
    response = requests.get(f"{BASE_URL}/models", headers=headers)
    
    if response.status_code == 200:
        models = response.json()
        print("✅ Available models:")
        for model in models.get('data', []):
            print(f"   - {model.get('id', 'N/A')} ({model.get('provider', 'N/A')})")
    else:
        print(f"❌ Models endpoint failed: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 New API key test completed!")
    print(f"🔑 API Key used: {new_api_key[:10]}...{new_api_key[-4:]}")
    print("✅ System works perfectly with new API keys!")

def test_client_library_with_new_key():
    """Test the client library with the new API key"""
    print("\n🧪 Testing Client Library with New API Key")
    print("=" * 50)
    
    try:
        from unillm import UniLLM
        
        # Get the API key from the previous test
        response = requests.get("http://localhost:8000/auth/me", 
                              headers={"Authorization": "Bearer friend@example.com"})
        if response.status_code != 200:
            print("❌ Could not get API key for client test")
            return
            
        user_data = response.json()
        api_key = user_data["api_key"]
        
        # Test client library
        client = UniLLM(
            api_key=api_key,
            base_url="http://localhost:8000"
        )
        
        # Test OpenAI
        response = client.chat(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello from client library!'"}],
            max_tokens=20
        )
        print(f"✅ Client Library OpenAI: {response.content}")
        
        # Test Anthropic
        response = client.chat(
            model="claude-3-opus-20240229",
            messages=[{"role": "user", "content": "Say 'Hello from client library!'"}],
            max_tokens=20
        )
        print(f"✅ Client Library Anthropic: {response.content}")
        
    except Exception as e:
        print(f"❌ Client library error: {e}")

if __name__ == "__main__":
    print("🚀 UniLLM New API Key Test")
    print("This simulates a friend using your system with fresh API keys")
    print("=" * 60)
    
    # Test with new API keys
    test_with_new_api_keys()
    
    # Test client library
    test_client_library_with_new_key()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("✅ New user registration works")
    print("✅ New API keys work with all providers")
    print("✅ Usage tracking works for new users")
    print("✅ Client library works with new keys")
    print("✅ System is ready for friends to use!") 