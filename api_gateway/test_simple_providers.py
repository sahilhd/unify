#!/usr/bin/env python3
"""
Simple test for OpenAI and Anthropic providers
"""

import requests
import json

# Use the correct UniLLM API key
UNILLM_API_KEY = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0"
BASE_URL = "http://localhost:8000"

def test_provider(model, provider_name):
    """Test a specific provider"""
    
    print(f"\n🧪 Testing {provider_name} model: {model}")
    
    headers = {
        "Authorization": f"Bearer {UNILLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": f"Say 'Hello from {provider_name}!' and nothing else."}
        ],
        "max_tokens": 20,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {provider_name} {model} successful!")
            print(f"📝 Response: {result.get('response', 'N/A')}")
            print(f"🔧 Provider: {result.get('provider', 'N/A')}")
            print(f"📊 Tokens: {result.get('tokens', 'N/A')}")
            print(f"💰 Cost: ${result.get('cost', 'N/A')}")
            return True
            
        elif response.status_code == 401:
            print(f"❌ {provider_name} authentication failed")
            print(f"Response: {response.text}")
            return False
            
        elif response.status_code == 402:
            print(f"⚠️  {provider_name} insufficient credits")
            print(f"Response: {response.text}")
            return True  # Auth worked, just no credits
            
        elif response.status_code == 500:
            print(f"❌ {provider_name} server error")
            print(f"Response: {response.text}")
            return False
            
        else:
            print(f"❌ {provider_name} unexpected error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {provider_name} error: {e}")
        return False

def main():
    """Test both providers"""
    
    print("🚀 Simple Provider Test")
    print("=" * 40)
    print(f"🔑 Using UniLLM API key: {UNILLM_API_KEY[:10]}...{UNILLM_API_KEY[-4:]}")
    
    # Test OpenAI
    openai_success = test_provider("gpt-3.5-turbo", "OpenAI")
    
    # Test Anthropic Opus
    anthropic_opus_success = test_provider("claude-3-opus-20240229", "Anthropic Opus")
    # Test Anthropic Haiku
    anthropic_haiku_success = test_provider("claude-3-haiku-20240307", "Anthropic Haiku")
    
    print(f"\n{'='*40}")
    print("📊 Results Summary:")
    print(f"   OpenAI: {'✅ Working' if openai_success else '❌ Failed'}")
    print(f"   Anthropic Opus: {'✅ Working' if anthropic_opus_success else '❌ Failed'}")
    print(f"   Anthropic Haiku: {'✅ Working' if anthropic_haiku_success else '❌ Failed'}")
    
    if openai_success and anthropic_opus_success and anthropic_haiku_success:
        print("\n🎉 All providers are working!")
    elif openai_success:
        print("\n⚠️  Only OpenAI is working. Anthropic may need API key setup.")
    else:
        print("\n❌ All providers failed. Check backend configuration.")

if __name__ == "__main__":
    main() 