#!/usr/bin/env python3
"""
Debug script to test UniLLM client directly
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to Python path
sys.path.insert(0, '../src')

# Load environment variables
load_dotenv()

def test_environment():
    """Test if environment variables are loaded"""
    print("🧪 Testing Environment Variables...")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print(f"✅ OpenAI API Key found: {openai_key[:20]}...")
    else:
        print("❌ OpenAI API Key not found")
        return False
    
    return True

def test_unillm_client():
    """Test UniLLM client directly"""
    print("\n🧪 Testing UniLLM Client...")
    
    try:
        from unillm import UniLLMClient
        
        # Initialize client
        client = UniLLMClient()
        print("✅ UniLLM client initialized")
        
        # Test a simple chat request
        print("ℹ️  Making test chat request...")
        
        response = client.chat(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello from UniLLM!' and nothing else."}
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        print("✅ Chat request successful!")
        print(f"ℹ️  Content: {response.content}")
        print(f"ℹ️  Model: {response.model}")
        print(f"ℹ️  Provider: {response.provider}")
        print(f"ℹ️  Usage: {response.usage}")
        
        return True
        
    except Exception as e:
        print(f"❌ UniLLM client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_openai_direct():
    """Test OpenAI API directly"""
    print("\n🧪 Testing OpenAI API Directly...")
    
    try:
        import openai
        
        # Set API key
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Test direct OpenAI call
        print("ℹ️  Making direct OpenAI API call...")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello from OpenAI!' and nothing else."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        print("✅ Direct OpenAI API call successful!")
        print(f"ℹ️  Response: {response.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct OpenAI API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all debug tests"""
    print("🚀 UniLLM Debug Test")
    print("=" * 50)
    
    # Test environment
    if not test_environment():
        print("\n❌ Environment not properly configured.")
        return
    
    # Test direct OpenAI API
    if not test_openai_direct():
        print("\n❌ Direct OpenAI API test failed.")
        return
    
    # Test UniLLM client
    if not test_unillm_client():
        print("\n❌ UniLLM client test failed.")
        return
    
    print("\n🎯 All tests completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main() 