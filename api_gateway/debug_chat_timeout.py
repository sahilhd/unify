"""
Debug script to test chat completions and identify timeout issues
"""

import requests
import time
import json

def test_chat_with_timeout():
    """Test chat completion with different timeouts"""
    
    print("🔍 Debugging Chat Timeout Issues")
    print("=" * 40)
    
    # First, register a user to get an API key
    email = f"debug_{int(time.time())}@example.com"
    password = "debugpass123"
    
    print(f"📧 Registering user: {email}")
    
    try:
        # Register
        register_response = requests.post(
            "http://localhost:8000/auth/register",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if register_response.status_code == 200:
            user_data = register_response.json()
            api_key = user_data["api_key"]
            print(f"✅ Registered successfully")
            print(f"   API Key: {api_key[:20]}...")
            
            # Test 1: Simple chat with short timeout
            print("\n🧪 Test 1: Simple chat (5s timeout)")
            try:
                chat_response = requests.post(
                    "http://localhost:8000/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": "Hi"}],
                        "max_tokens": 5
                    },
                    timeout=5
                )
                print(f"   Status: {chat_response.status_code}")
                if chat_response.status_code == 200:
                    print(f"   Response: {chat_response.json()}")
                else:
                    print(f"   Error: {chat_response.text}")
            except requests.exceptions.Timeout:
                print("   ❌ Timeout after 5 seconds")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 2: Chat with longer timeout
            print("\n🧪 Test 2: Chat with longer timeout (15s)")
            try:
                chat_response = requests.post(
                    "http://localhost:8000/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": "Hello world"}],
                        "max_tokens": 10
                    },
                    timeout=15
                )
                print(f"   Status: {chat_response.status_code}")
                if chat_response.status_code == 200:
                    print(f"   Response: {chat_response.json()}")
                else:
                    print(f"   Error: {chat_response.text}")
            except requests.exceptions.Timeout:
                print("   ❌ Timeout after 15 seconds")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 3: Usage stats
            print("\n🧪 Test 3: Usage stats")
            try:
                usage_response = requests.get(
                    "http://localhost:8000/billing/usage",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10
                )
                print(f"   Status: {usage_response.status_code}")
                if usage_response.status_code == 200:
                    print(f"   Response: {usage_response.json()}")
                else:
                    print(f"   Error: {usage_response.text}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Error: {register_response.text}")
            
    except Exception as e:
        print(f"❌ Error during registration: {e}")

if __name__ == "__main__":
    test_chat_with_timeout() 