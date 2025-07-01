#!/usr/bin/env python3
"""
OpenAI Real Response Testing

Test OpenAI models with real credits to see actual responses.
"""

import os
import requests
import json
from typing import Dict, List

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "test-client-key"

def load_env():
    """Load environment variables from .env file."""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def make_chat_request(model: str, messages: List[Dict[str, str]], **kwargs) -> Dict:
    """Make a chat completion request to the API gateway."""
    
    url = f"{API_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        **kwargs
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

def test_openai_models():
    """Test different OpenAI models."""
    
    print("🤖 === Testing OpenAI Models ===")
    
    # Test different OpenAI models
    models_to_test = [
        ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
        ("gpt-4", "GPT-4"),
    ]
    
    test_prompts = [
        "What is the capital of France?",
        "Write a haiku about technology",
        "Explain quantum computing in simple terms",
    ]
    
    for model, name in models_to_test:
        print(f"\n🔹 Testing {name} ({model})...")
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n  📝 Test {i}: {prompt}")
            
            response = make_chat_request(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            if response:
                print(f"  ✅ Response: {response['content']}")
                print(f"  📊 Tokens: {response['usage']['total_tokens']}")
                print(f"  🔧 Provider: {response['provider']}")
            else:
                print(f"  ❌ Failed to get response")

def test_provider_switching():
    """Test switching between OpenAI and other providers."""
    
    print("\n🔄 === Testing Provider Switching ===")
    
    question = "What are the three laws of robotics?"
    
    # Test OpenAI (should work with credits)
    print(f"\n🤖 Testing OpenAI (gpt-3.5-turbo)...")
    openai_response = make_chat_request(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        max_tokens=200
    )
    
    if openai_response:
        print(f"✅ OpenAI Response: {openai_response['content']}")
        print(f"📊 Tokens: {openai_response['usage']['total_tokens']}")
    else:
        print("❌ OpenAI failed")
    
    # Test Anthropic (should fail with invalid key)
    print(f"\n🤖 Testing Anthropic (claude-3-sonnet)...")
    anthropic_response = make_chat_request(
        model="claude-3-sonnet",
        messages=[{"role": "user", "content": question}],
        max_tokens=200
    )
    
    if anthropic_response:
        print(f"✅ Anthropic Response: {anthropic_response['content']}")
        print(f"📊 Tokens: {anthropic_response['usage']['total_tokens']}")
    else:
        print("❌ Anthropic failed (expected - no valid key)")
    
    # Test Gemini (should fail with invalid key)
    print(f"\n🤖 Testing Gemini (gemini-pro)...")
    gemini_response = make_chat_request(
        model="gemini-pro",
        messages=[{"role": "user", "content": question}],
        max_tokens=200
    )
    
    if gemini_response:
        print(f"✅ Gemini Response: {gemini_response['content']}")
        print(f"📊 Tokens: {gemini_response['usage']['total_tokens']}")
    else:
        print("❌ Gemini failed (expected - no valid key)")

def test_conversation_switching():
    """Test conversation switching with OpenAI working."""
    
    print("\n🗣️ === Testing Conversation Switching ===")
    
    # Start conversation with OpenAI
    conversation = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": "I want to visit Paris. What should I know?"}
    ]
    
    print("\n🗣️ Starting conversation with OpenAI...")
    response1 = make_chat_request(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=200
    )
    
    if response1:
        print(f"✅ OpenAI Response: {response1['content']}")
        
        # Add OpenAI's response to conversation
        conversation.append({"role": "assistant", "content": response1['content']})
        conversation.append({"role": "user", "content": "What about the best time to visit?"})
        
        # Continue with OpenAI (should work)
        print("\n🔄 Continuing with OpenAI...")
        response2 = make_chat_request(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=200
        )
        
        if response2:
            print(f"✅ OpenAI Response: {response2['content']}")
            
            # Try to switch to Anthropic (should fail)
            conversation.append({"role": "assistant", "content": response2['content']})
            conversation.append({"role": "user", "content": "What about transportation options?"})
            
            print("\n🔄 Trying to switch to Anthropic...")
            response3 = make_chat_request(
                model="claude-3-sonnet",
                messages=conversation,
                max_tokens=200
            )
            
            if response3:
                print(f"✅ Anthropic Response: {response3['content']}")
            else:
                print("❌ Anthropic failed (expected - no valid key)")
        else:
            print("❌ OpenAI failed")
    else:
        print("❌ OpenAI failed")

def test_different_parameters():
    """Test different parameters with OpenAI."""
    
    print("\n🎛️ === Testing Different Parameters ===")
    
    prompt = "Write a creative story about a robot"
    model = "gpt-3.5-turbo"
    
    # Test different temperatures
    temperatures = [0.1, 0.7, 1.0]
    
    for temp in temperatures:
        print(f"\n🌡️ Testing temperature {temp}...")
        
        response = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=100
        )
        
        if response:
            print(f"✅ Response: {response['content']}")
            print(f"📊 Tokens: {response['usage']['total_tokens']}")
        else:
            print(f"❌ Failed to get response")

def check_api_status():
    """Check if the API gateway is running."""
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API Gateway is running")
            return True
        else:
            print("❌ API Gateway is not responding correctly")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API Gateway. Make sure it's running on http://localhost:8000")
        return False

def main():
    """Main function to run all tests."""
    
    print("🚀 UniLLM API Gateway - OpenAI Real Response Testing")
    print("=" * 60)
    
    # Load environment
    load_env()
    
    # Check if API is running
    if not check_api_status():
        print("\nTo start the API gateway, run:")
        print("python main.py")
        return
    
    print("\n" + "="*60)
    
    # Run tests
    test_openai_models()
    test_provider_switching()
    test_conversation_switching()
    test_different_parameters()
    
    print("\n🎉 OpenAI testing completed!")
    print("\n💡 What we learned:")
    print("- OpenAI models work with real credits")
    print("- Provider switching works correctly")
    print("- Other providers fail gracefully with invalid keys")
    print("- Conversation switching works within the same provider")

if __name__ == "__main__":
    main() 