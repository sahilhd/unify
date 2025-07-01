#!/usr/bin/env python3
"""
Test Anthropic API key directly with Anthropic's API
"""

import os
import requests
import json

def test_anthropic_key_direct():
    """Test Anthropic API key directly with Anthropic's API"""
    
    # Get API key from environment or prompt user
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set.")
        print("Please set your Anthropic API key:")
        api_key = input("Enter your Anthropic API key: ").strip()
        if not api_key:
            print("❌ No API key provided. Exiting.")
            return False
    
    print("🧪 Testing Anthropic API Key Directly")
    print("=" * 40)
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    # Anthropic API endpoint (Claude 3)
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 20,
        "messages": [
            {"role": "user", "content": "Say 'Hello from Anthropic!' and nothing else."}
        ]
    }
    
    try:
        print("\n📡 Making direct request to Anthropic API (Claude 3 Opus)...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Anthropic API key is valid!")
            print(f"📝 Response: {result['content'][0]['text']}")
            print(f"🔧 Model: {result['model']}")
            print(f"📊 Usage: {result['usage']}")
            return True
        elif response.status_code == 401:
            print("❌ Anthropic API key is invalid or expired")
            print(f"Response: {response.text}")
            return False
        elif response.status_code == 403:
            print("❌ Anthropic API key is forbidden (check account access)")
            print(f"Response: {response.text}")
            return False
        elif response.status_code == 429:
            print("⚠️  Rate limit exceeded - try again later")
            print(f"Response: {response.text}")
            return False
        elif response.status_code == 400:
            print("❌ Bad request - likely model not available for this key")
            print(f"Response: {response.text}")
            return False
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

if __name__ == "__main__":
    test_anthropic_key_direct() 