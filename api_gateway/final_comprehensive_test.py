"""
Final Comprehensive Test for UniLLM
Tests all major functionality to ensure everything is working
"""

import requests
import time
import json
from unillm_client_library import UniLLMClient

def comprehensive_test():
    """Run comprehensive tests on all UniLLM functionality"""
    
    print("🎯 UniLLM Comprehensive Test")
    print("=" * 50)
    
    # Test 1: Server Health
    print("\n1️⃣ Testing Server Health")
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Server is healthy")
            print(f"   Version: {health_data.get('version')}")
            print(f"   Features: {health_data.get('features')}")
        else:
            print(f"❌ Server health check failed: {health_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Server health check error: {e}")
        return
    
    # Test 2: User Registration and API Key
    print("\n2️⃣ Testing User Registration")
    email = f"comprehensive_{int(time.time())}@example.com"
    password = "testpass123"
    
    try:
        register_response = requests.post(
            "http://localhost:8000/auth/register",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if register_response.status_code == 200:
            user_data = register_response.json()
            api_key = user_data["api_key"]
            print(f"✅ User registered successfully")
            print(f"   Email: {email}")
            print(f"   API Key: {api_key[:20]}...")
            print(f"   Initial Credits: {user_data.get('credits', 0)}")
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Error: {register_response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 3: Client Library
    print("\n3️⃣ Testing Client Library")
    try:
        client = UniLLMClient(api_key)
        
        # Test chat completion
        response = client.ChatCompletion().create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'UniLLM is working!'"}],
            max_tokens=10
        )
        
        print(f"✅ Client library chat successful")
        print(f"   Response: {response.choices[0].message.content}")
        print(f"   Usage: {response.usage.total_tokens} tokens")
        
        # Test usage stats
        usage = client.get_usage_stats()
        print(f"✅ Usage stats retrieved")
        print(f"   Total requests: {usage.get('total_requests', 0)}")
        print(f"   Total cost: ${usage.get('total_cost', 0):.6f}")
        
    except Exception as e:
        print(f"❌ Client library error: {e}")
    
    # Test 4: Direct API Calls
    print("\n4️⃣ Testing Direct API Calls")
    try:
        # Test chat completion
        chat_response = requests.post(
            "http://localhost:8000/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4-turbo",
                "messages": [{"role": "user", "content": "What is 2+2?"}],
                "max_tokens": 5
            },
            timeout=15
        )
        
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            print(f"✅ Direct API chat successful")
            print(f"   Response: {chat_data.get('response', 'N/A')}")
            print(f"   Provider: {chat_data.get('provider', 'N/A')}")
            print(f"   Cost: ${chat_data.get('cost', 0):.6f}")
            print(f"   Remaining credits: {chat_data.get('remaining_credits', 0)}")
        else:
            print(f"❌ Direct API chat failed: {chat_response.status_code}")
            print(f"   Error: {chat_response.text}")
        
        # Test usage stats
        usage_response = requests.get(
            "http://localhost:8000/billing/usage",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        
        if usage_response.status_code == 200:
            usage_data = usage_response.json()
            print(f"✅ Direct API usage stats successful")
            print(f"   Total requests: {usage_data.get('total_requests', 0)}")
            print(f"   Total tokens: {usage_data.get('total_tokens', 0)}")
            print(f"   Total cost: ${usage_data.get('total_cost', 0):.6f}")
        else:
            print(f"❌ Direct API usage stats failed: {usage_response.status_code}")
            print(f"   Error: {usage_response.text}")
            
    except Exception as e:
        print(f"❌ Direct API error: {e}")
    
    # Test 5: Credit Purchase
    print("\n5️⃣ Testing Credit Purchase")
    try:
        purchase_response = requests.post(
            "http://localhost:8000/billing/purchase-credits",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={"credits": 25.0},
            timeout=10
        )
        
        if purchase_response.status_code == 200:
            purchase_data = purchase_response.json()
            print(f"✅ Credit purchase successful")
            print(f"   Credits added: {purchase_data.get('credits_added', 0)}")
            print(f"   New balance: {purchase_data.get('new_balance', 0)}")
        else:
            print(f"❌ Credit purchase failed: {purchase_response.status_code}")
            print(f"   Error: {purchase_response.text}")
            
    except Exception as e:
        print(f"❌ Credit purchase error: {e}")
    
    # Test 6: Provider Switching
    print("\n6️⃣ Testing Provider Switching")
    try:
        # Test OpenAI
        openai_response = requests.post(
            "http://localhost:8000/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "OpenAI test"}],
                "max_tokens": 5
            },
            timeout=15
        )
        
        if openai_response.status_code == 200:
            openai_data = openai_response.json()
            print(f"✅ OpenAI provider working")
            print(f"   Provider: {openai_data.get('provider', 'N/A')}")
        else:
            print(f"❌ OpenAI provider failed: {openai_response.status_code}")
        
        # Test Anthropic (should fail without API key, but gracefully)
        anthropic_response = requests.post(
            "http://localhost:8000/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "claude-3-sonnet",
                "messages": [{"role": "user", "content": "Anthropic test"}],
                "max_tokens": 5
            },
            timeout=15
        )
        
        if anthropic_response.status_code == 500:
            error_data = anthropic_response.json()
            if "Authentication failed" in error_data.get('detail', ''):
                print(f"✅ Anthropic provider correctly rejected (no API key)")
            else:
                print(f"❌ Anthropic provider unexpected error: {error_data}")
        else:
            print(f"❌ Anthropic provider unexpected response: {anthropic_response.status_code}")
            
    except Exception as e:
        print(f"❌ Provider switching error: {e}")
    
    print("\n🎉 Comprehensive Test Completed!")
    print(f"📧 Test user: {email}")
    print(f"🔑 API Key: {api_key[:20]}...")

if __name__ == "__main__":
    comprehensive_test() 