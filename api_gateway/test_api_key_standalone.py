#!/usr/bin/env python3
"""
Standalone UniLLM API Key Test
Use this script to test your UniLLM API key in a fresh project.
Just copy and paste your API key and run this script.
"""

import requests
import json
import time

def test_unillm_api_key(api_key: str, base_url: str = "http://localhost:8000"):
    """
    Test a UniLLM API key with a simple chat request
    
    Args:
        api_key: Your UniLLM API key (starts with 'unillm_')
        base_url: The UniLLM server URL (default: localhost:8000)
    """
    
    print(f"🔑 Testing UniLLM API Key: {api_key[:20]}...")
    print(f"🌐 Server URL: {base_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing server health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Server is healthy!")
            print(f"   Version: {health_data.get('version', 'N/A')}")
            print(f"   Features: {', '.join(health_data.get('features', []))}")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    
    # Test 2: Chat Completion
    print("\n2️⃣ Testing chat completion...")
    chat_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'Hello from UniLLM!' in exactly 5 words."}
        ],
        "max_tokens": 20
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat completion successful!")
            print(f"   Response: {result.get('response', 'N/A')}")
            print(f"   Provider: {result.get('provider', 'N/A')}")
            print(f"   Cost: {result.get('cost', 'N/A')}")
            print(f"   Remaining Credits: {result.get('remaining_credits', 'N/A')}")
        else:
            print(f"❌ Chat completion failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat request failed: {e}")
        return False
    
    # Test 3: Usage Stats
    print("\n3️⃣ Testing usage stats...")
    try:
        response = requests.get(
            f"{base_url}/billing/usage",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            usage_data = response.json()
            print("✅ Usage stats retrieved!")
            print(f"   Total Requests: {usage_data.get('total_requests', 'N/A')}")
            print(f"   Total Cost: {usage_data.get('total_cost', 'N/A')}")
            print(f"   Requests Today: {usage_data.get('requests_today', 'N/A')}")
        else:
            print(f"❌ Usage stats failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Usage stats request failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API Key test completed!")
    return True

def main():
    """Main function to run the test"""
    print("🚀 UniLLM API Key Standalone Test")
    print("=" * 60)
    
    # Get API key from user
    print("\n📋 Instructions:")
    print("1. Copy your UniLLM API key (starts with 'unillm_')")
    print("2. Paste it below when prompted")
    print("3. Make sure your UniLLM server is running on localhost:8000")
    print("\n" + "-" * 40)
    
    # Get API key
    api_key = input("🔑 Enter your UniLLM API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided!")
        return
    
    if not api_key.startswith("unillm_"):
        print("❌ Invalid API key format! Should start with 'unillm_'")
        return
    
    # Get server URL (optional)
    server_url = input("🌐 Enter server URL (default: http://localhost:8000): ").strip()
    if not server_url:
        server_url = "http://localhost:8000"
    
    print(f"\n🚀 Starting test with key: {api_key[:20]}...")
    print(f"🌐 Server: {server_url}")
    
    # Run the test
    success = test_unillm_api_key(api_key, server_url)
    
    if success:
        print("\n✅ Your API key is working correctly!")
        print("💡 You can now use this API key in your applications.")
    else:
        print("\n❌ API key test failed!")
        print("💡 Check that:")
        print("   - Your UniLLM server is running")
        print("   - The API key is correct")
        print("   - You have sufficient credits")

if __name__ == "__main__":
    main() 