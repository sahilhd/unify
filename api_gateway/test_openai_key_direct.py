#!/usr/bin/env python3
"""
Test OpenAI API key directly with OpenAI's API
"""

import os
import requests
import json

def test_openai_key_direct():
    """Test OpenAI API key directly with OpenAI's API"""
    
    # Get API key from environment or prompt user
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key:")
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key:
            print("❌ No API key provided. Exiting.")
            return False
    
    print("🧪 Testing OpenAI API Key Directly")
    print("=" * 40)
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    # Test with OpenAI's API directly
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'Hello from OpenAI!' and nothing else."}
        ],
        "max_tokens": 20,
        "temperature": 0.7
    }
    
    try:
        print("\n📡 Making direct request to OpenAI API...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            usage = result['usage']
            
            print("✅ OpenAI API key is valid!")
            print(f"📝 Response: {content}")
            print(f"📊 Tokens used: {usage['total_tokens']}")
            print(f"💰 Cost estimate: ~${usage['total_tokens'] * 0.000002:.6f}")
            return True
            
        elif response.status_code == 401:
            print("❌ OpenAI API key is invalid or expired")
            print(f"Response: {response.text}")
            return False
            
        elif response.status_code == 429:
            print("⚠️  Rate limit exceeded - try again later")
            print(f"Response: {response.text}")
            return False
            
        elif response.status_code == 402:
            print("⚠️  Insufficient credits/quota")
            print(f"Response: {response.text}")
            return True  # Key is valid, just no credits
            
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check your internet connection")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_openai_models():
    """Test what models are available with this API key"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set. Skipping model test.")
        return
    
    print("\n🔍 Testing available OpenAI models...")
    
    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            models = response.json()
            chat_models = [model['id'] for model in models['data'] 
                          if 'gpt' in model['id'].lower()]
            
            print("✅ Available chat models:")
            for model in sorted(chat_models):
                print(f"   • {model}")
        else:
            print(f"❌ Failed to get models: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting models: {e}")

if __name__ == "__main__":
    success = test_openai_key_direct()
    if success:
        test_openai_models()
    
    print(f"\n{'='*40}")
    if success:
        print("🎉 OpenAI API key test completed successfully!")
    else:
        print("❌ OpenAI API key test failed!") 