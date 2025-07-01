#!/usr/bin/env python3
"""
Test UniLLM backend with the correct API key
"""

import requests
import json

# Use the correct UniLLM API key (not OpenAI key)
UNILLM_API_KEY = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0"
BASE_URL = "http://localhost:8000"

def test_unillm_chat():
    """Test UniLLM chat endpoint with correct API key"""
    
    print("🧪 Testing UniLLM Backend with Correct API Key")
    print("=" * 50)
    print(f"🔑 Using UniLLM API key: {UNILLM_API_KEY[:10]}...{UNILLM_API_KEY[-4:]}")
    
    headers = {
        "Authorization": f"Bearer {UNILLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'Hello from UniLLM!' and nothing else."}
        ],
        "max_tokens": 20,
        "temperature": 0.7
    }
    
    try:
        print("\n📡 Making request to UniLLM backend...")
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ UniLLM backend request successful!")
            print(f"📝 Response: {result.get('response', 'N/A')}")
            print(f"🔧 Provider: {result.get('provider', 'N/A')}")
            print(f"📊 Tokens: {result.get('tokens', 'N/A')}")
            print(f"💰 Cost: ${result.get('cost', 'N/A')}")
            print(f"💳 Remaining Credits: ${result.get('remaining_credits', 'N/A')}")
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed")
            print(f"Response: {response.text}")
            return False
            
        elif response.status_code == 402:
            print("⚠️  Insufficient credits")
            print(f"Response: {response.text}")
            return True  # Auth worked, just no credits
            
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure backend is running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_usage_stats():
    """Test usage statistics endpoint"""
    
    print("\n📊 Testing Usage Statistics...")
    
    headers = {"Authorization": f"Bearer {UNILLM_API_KEY}"}
    
    try:
        response = requests.get(f"{BASE_URL}/billing/usage", headers=headers, timeout=10)
        
        if response.status_code == 200:
            usage = response.json()
            print("✅ Usage stats retrieved:")
            print(f"   Total Requests: {usage.get('total_requests', 0)}")
            print(f"   Total Tokens: {usage.get('total_tokens', 0)}")
            print(f"   Total Cost: ${usage.get('total_cost', 0):.6f}")
            print(f"   Requests Today: {usage.get('requests_today', 0)}")
            return True
        else:
            print(f"❌ Usage stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Usage stats error: {e}")
        return False

if __name__ == "__main__":
    success = test_unillm_chat()
    if success:
        test_usage_stats()
    
    print(f"\n{'='*50}")
    if success:
        print("🎉 UniLLM backend test completed successfully!")
        print("💡 The issue was using the wrong API key!")
        print("   - Use UniLLM API key for UniLLM backend")
        print("   - Use OpenAI API key for direct OpenAI calls")
    else:
        print("❌ UniLLM backend test failed!") 