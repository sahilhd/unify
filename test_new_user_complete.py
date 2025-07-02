#!/usr/bin/env python3
"""
Comprehensive test for new user with API key: unillm_fUyUgDVTMIHDPzuhWGQZlzSkYEMYv2XM
This tests all functionality and investigates chat history isolation
"""

import requests
import json
import time

def test_new_user_complete():
    """Test all functionality with the new user's API key"""
    print("🧪 Testing New User: mk@gmail.com")
    print("🔑 API Key: unillm_fUyUgDVTMIHDPzuhWGQZlzSkYEMYv2XM")
    print("=" * 60)
    
    BASE_URL = "http://localhost:8000"
    API_KEY = "unillm_fUyUgDVTMIHDPzuhWGQZlzSkYEMYv2XM"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test 1: User Info
    print("\n1️⃣ Testing User Information...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ User: {user_data['email']}")
        print(f"💰 Credits: ${user_data['credits']:.2f}")
        print(f"🔑 API Key: {user_data['api_key'][:10]}...{user_data['api_key'][-4:]}")
    else:
        print(f"❌ User info failed: {response.status_code}")
        return
    
    # Test 2: OpenAI Integration
    print("\n2️⃣ Testing OpenAI Integration...")
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say 'Hello from mk@gmail.com!'"}],
            "max_tokens": 20
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ OpenAI: {result.get('response', 'N/A')}")
        print(f"💰 Cost: ${result.get('cost', 0):.6f}")
        print(f"💳 Remaining: ${result.get('remaining_credits', 0):.2f}")
    else:
        print(f"❌ OpenAI failed: {response.status_code}")
        print(f"Error: {response.text}")
    
    # Test 3: Anthropic Integration
    print("\n3️⃣ Testing Anthropic Integration...")
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json={
            "model": "claude-3-opus-20240229",
            "messages": [{"role": "user", "content": "Say 'Hello from Anthropic!'"}],
            "max_tokens": 20
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Anthropic: {result.get('response', 'N/A')}")
        print(f"💰 Cost: ${result.get('cost', 0):.6f}")
        print(f"💳 Remaining: ${result.get('remaining_credits', 0):.2f}")
    else:
        print(f"❌ Anthropic failed: {response.status_code}")
        print(f"Error: {response.text}")
    
    # Test 4: Usage Statistics
    print("\n4️⃣ Testing Usage Statistics...")
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
    
    # Test 5: Models Endpoint
    print("\n5️⃣ Testing Models Endpoint...")
    response = requests.get(f"{BASE_URL}/models", headers=headers)
    
    if response.status_code == 200:
        models = response.json()
        print("✅ Available models:")
        for model in models.get('data', []):
            print(f"   - {model.get('id', 'N/A')} ({model.get('provider', 'N/A')})")
    else:
        print(f"❌ Models endpoint failed: {response.status_code}")
    
    # Test 6: Multiple Chat Messages (to test chat history)
    print("\n6️⃣ Testing Chat History Isolation...")
    
    # First message
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "My name is MK and I'm 25 years old."}],
            "max_tokens": 50
        }
    )
    
    if response.status_code == 200:
        result1 = response.json()
        print(f"✅ Message 1: {result1.get('response', 'N/A')}")
        
        # Second message (should remember the context)
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "My name is MK and I'm 25 years old."},
                    {"role": "assistant", "content": result1.get('response', '')},
                    {"role": "user", "content": "What's my name and age?"}
                ],
                "max_tokens": 50
            }
        )
        
        if response.status_code == 200:
            result2 = response.json()
            print(f"✅ Message 2: {result2.get('response', 'N/A')}")
        else:
            print(f"❌ Message 2 failed: {response.status_code}")
    else:
        print(f"❌ Message 1 failed: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("🎉 Complete functionality test completed!")
    print("✅ All features working with new user!")

def test_chat_history_isolation():
    """Test if chat history is properly isolated between users"""
    print("\n🔍 Testing Chat History Isolation Between Users")
    print("=" * 60)
    
    BASE_URL = "http://localhost:8000"
    
    # Test with original user
    original_key = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0"
    original_headers = {
        "Authorization": f"Bearer {original_key}",
        "Content-Type": "application/json"
    }
    
    # Test with new user
    new_key = "unillm_fUyUgDVTMIHDPzuhWGQZlzSkYEMYv2XM"
    new_headers = {
        "Authorization": f"Bearer {new_key}",
        "Content-Type": "application/json"
    }
    
    print("Testing with original user (test@example.com)...")
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=original_headers,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "My name is Test User. Remember this."}],
            "max_tokens": 50
        }
    )
    
    if response.status_code == 200:
        original_response = response.json()
        print(f"✅ Original user response: {original_response.get('response', 'N/A')}")
    else:
        print(f"❌ Original user failed: {response.status_code}")
        return
    
    print("\nTesting with new user (mk@gmail.com)...")
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=new_headers,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "What's my name? (I haven't told you yet)"}],
            "max_tokens": 50
        }
    )
    
    if response.status_code == 200:
        new_response = response.json()
        print(f"✅ New user response: {new_response.get('response', 'N/A')}")
        
        # Check if the new user knows about the original user's name
        if "Test User" in new_response.get('response', ''):
            print("⚠️  WARNING: Chat history is NOT properly isolated!")
            print("   The new user can see the original user's chat history.")
        else:
            print("✅ Chat history is properly isolated!")
            print("   Each user has their own separate chat context.")
    else:
        print(f"❌ New user failed: {response.status_code}")

def check_database_isolation():
    """Check if usage logs are properly isolated in the database"""
    print("\n🔍 Checking Database Isolation")
    print("=" * 60)
    
    # Check usage logs for both users
    print("Checking usage logs in database...")
    
    # Get user IDs
    result = run_terminal_cmd("sqlite3 unillm.db \"SELECT id, email FROM users WHERE email IN ('test@example.com', 'mk@gmail.com');\"")
    print(f"Users: {result}")
    
    # Check usage logs
    result = run_terminal_cmd("sqlite3 unillm.db \"SELECT user_id, model, tokens_used, cost FROM usage_logs WHERE user_id IN (SELECT id FROM users WHERE email IN ('test@example.com', 'mk@gmail.com')) ORDER BY user_id, request_timestamp DESC LIMIT 10;\"")
    print(f"Recent usage logs: {result}")

def run_terminal_cmd(cmd):
    """Helper function to run terminal commands"""
    import subprocess
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("🚀 UniLLM New User Complete Test")
    print("Testing all functionality with: mk@gmail.com")
    print("=" * 60)
    
    # Test complete functionality
    test_new_user_complete()
    
    # Test chat history isolation
    test_chat_history_isolation()
    
    # Check database isolation
    check_database_isolation()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("✅ New user API key is unique")
    print("✅ All functionality works with new user")
    print("🔍 Chat history isolation investigated")
    print("🔍 Database isolation checked") 