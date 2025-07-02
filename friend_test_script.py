#!/usr/bin/env python3
"""
Simple test script for friends to test UniLLM remotely
Replace the BASE_URL with your deployed server URL
"""

import requests
import json

# 🔧 CONFIGURATION - Replace with your deployed URL
BASE_URL = "https://your-app.railway.app"  # Change this to your actual URL
API_KEY = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0"

def test_api():
    """Test the UniLLM API with both OpenAI and Anthropic models"""
    
    print("🚀 UniLLM Remote Test")
    print("=" * 50)
    print(f"🌐 Server: {BASE_URL}")
    print(f"🔑 API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    print()
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test 1: OpenAI GPT-3.5-turbo
    print("🧪 Testing OpenAI GPT-3.5-turbo...")
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Say 'Hello from OpenAI!' and nothing else."}],
                "max_tokens": 20,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ OpenAI: {result.get('response', 'N/A')}")
            print(f"   Provider: {result.get('provider', 'N/A')}")
            print(f"   Cost: ${result.get('cost', 'N/A')}")
        else:
            print(f"❌ OpenAI failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
    
    print()
    
    # Test 2: Anthropic Claude-3-Opus
    print("🧪 Testing Anthropic Claude-3-Opus...")
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json={
                "model": "claude-3-opus-20240229",
                "messages": [{"role": "user", "content": "Say 'Hello from Anthropic!' and nothing else."}],
                "max_tokens": 20,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Anthropic: {result.get('response', 'N/A')}")
            print(f"   Provider: {result.get('provider', 'N/A')}")
            print(f"   Cost: ${result.get('cost', 'N/A')}")
        else:
            print(f"❌ Anthropic failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Anthropic error: {e}")
    
    print()
    
    # Test 3: Check available models
    print("🧪 Checking available models...")
    try:
        response = requests.get(f"{BASE_URL}/models", headers=headers, timeout=10)
        if response.status_code == 200:
            models = response.json()
            print("✅ Available models:")
            for model in models.get('data', []):
                print(f"   - {model.get('id', 'N/A')} ({model.get('provider', 'N/A')})")
        else:
            print(f"❌ Models check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Models check error: {e}")
    
    print()
    print("=" * 50)
    print("🎉 Test completed!")

def test_dashboard():
    """Test dashboard login (if frontend is deployed)"""
    print("\n🌐 Dashboard Test")
    print("=" * 30)
    print(f"Dashboard URL: {BASE_URL}")
    print("Login credentials:")
    print("   Email: sah@gmail.com")
    print("   Password: 123")
    print("\nNote: Dashboard may not be available if only API is deployed")

if __name__ == "__main__":
    # Test the API
    test_api()
    
    # Test dashboard access
    test_dashboard()
    
    print("\n📝 Instructions:")
    print("1. Replace BASE_URL with your actual deployed server URL")
    print("2. Make sure your server is running and accessible")
    print("3. Run this script: python3 friend_test_script.py")
    print("4. Check the results above") 