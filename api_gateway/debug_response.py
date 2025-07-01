"""
Debug the API response to fix the client library
"""

import requests
import time
import json

# Register a new user
email = f"test_{int(time.time())}@example.com"
password = "testpassword123"

print(f"📧 Registering user: {email}")

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
    
    # Test chat completion and see the raw response
    print("\n🔧 Testing chat completion...")
    chat_response = requests.post(
        "http://localhost:8000/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Say 'Hello from UniLLM!'"}
            ],
            "max_tokens": 20
        }
    )
    
    print(f"Status Code: {chat_response.status_code}")
    print(f"Raw Response: {chat_response.text}")
    
    if chat_response.status_code == 200:
        response_data = chat_response.json()
        print(f"\nParsed Response:")
        print(json.dumps(response_data, indent=2))
        
        # Check if choices exist
        if "choices" in response_data and len(response_data["choices"]) > 0:
            print(f"\n✅ Response has choices")
            print(f"First choice: {response_data['choices'][0]}")
        else:
            print(f"\n❌ No choices in response")
            
else:
    print(f"❌ Registration failed: {register_response.status_code}")
    print(f"   Response: {register_response.text}") 