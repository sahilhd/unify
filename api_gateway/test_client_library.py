"""
Test the UniLLM client library
"""

import os
import sys
from unillm_client_library import UniLLMClient, create_chat_completion

def test_client_library():
    """Test the client library functionality."""
    
    # Get API key from environment or use a test key
    api_key = os.getenv("UNILLM_API_KEY", "unillm_test_key")
    
    print("🧪 Testing UniLLM Client Library")
    print("=" * 40)
    
    try:
        # Test 1: Initialize client
        print("1️⃣ Testing client initialization...")
        client = UniLLMClient(api_key)
        print("✅ Client initialized successfully")
        
        # Test 2: Simple chat completion
        print("\n2️⃣ Testing chat completion...")
        response = client.ChatCompletion().create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello from UniLLM!'"}
            ],
            max_tokens=20
        )
        
        print(f"✅ Chat completion successful")
        print(f"   Response: {response.choices[0].message.content}")
        print(f"   Provider: {response.provider}")
        print(f"   Cost: ${response.cost:.6f}")
        print(f"   Remaining credits: {response.remaining_credits}")
        
        # Test 3: Usage stats
        print("\n3️⃣ Testing usage stats...")
        usage = client.get_usage_stats()
        print(f"✅ Usage stats retrieved")
        print(f"   Total requests: {usage.get('total_requests', 0)}")
        print(f"   Total tokens: {usage.get('total_tokens', 0)}")
        print(f"   Total cost: ${usage.get('total_cost', 0):.6f}")
        
        # Test 4: Convenience function
        print("\n4️⃣ Testing convenience function...")
        response2 = create_chat_completion(
            api_key=api_key,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "What's 2+2?"}
            ],
            max_tokens=10
        )
        
        print(f"✅ Convenience function works")
        print(f"   Response: {response2.choices[0].message.content}")
        
        # Test 5: Model switching
        print("\n5️⃣ Testing model switching...")
        response3 = client.ChatCompletion().create(
            model="claude-3-haiku-20240307",  # Try Anthropic
            messages=[
                {"role": "user", "content": "Say 'Hello from Claude!'"}
            ],
            max_tokens=20
        )
        
        print(f"✅ Model switching successful")
        print(f"   Response: {response3.choices[0].message.content}")
        print(f"   Provider: {response3.provider}")
        
        print("\n🎉 All tests passed! Client library is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_client_library()
    sys.exit(0 if success else 1) 