"""
Test the UniLLM client library with a real API key
"""

import os
import sys
from unillm_client_library import UniLLMClient

def test_with_real_key():
    """Test the client library with a real API key."""
    
    print("🧪 Testing UniLLM Client Library with Real API Key")
    print("=" * 55)
    
    # First, let's get a real API key by registering a user
    import requests
    import time
    
    # Register a new user
    email = f"test_{int(time.time())}@example.com"
    password = "testpassword123"
    
    print(f"📧 Registering user: {email}")
    
    try:
        # Register
        register_response = requests.post(
            "http://localhost:8000/auth/register",
            json={"email": email, "password": password}
        )
        
        if register_response.status_code == 200:
            user_data = register_response.json()
            api_key = user_data["api_key"]
            print(f"✅ Registered successfully")
            print(f"   API Key: {api_key[:20]}...")
            
            # Test the client library
            print("\n🔧 Testing client library...")
            client = UniLLMClient(api_key)
            
            # Test chat completion
            print("   Testing chat completion...")
            response = client.ChatCompletion().create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Say 'Hello from UniLLM!'"}
                ],
                max_tokens=20
            )
            
            print(f"✅ Chat completion successful!")
            print(f"   Response: {response.choices[0].message.content}")
            print(f"   Provider: {response.provider}")
            print(f"   Cost: ${response.cost:.6f}")
            print(f"   Remaining credits: {response.remaining_credits}")
            
            # Test usage stats
            print("\n   Testing usage stats...")
            usage = client.get_usage_stats()
            print(f"✅ Usage stats retrieved")
            print(f"   Total requests: {usage.get('total_requests', 0)}")
            print(f"   Total cost: ${usage.get('total_cost', 0):.6f}")
            
            print("\n🎉 Client library is working perfectly!")
            return True
            
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_with_real_key()
    sys.exit(0 if success else 1) 