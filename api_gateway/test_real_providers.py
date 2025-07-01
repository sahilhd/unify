#!/usr/bin/env python3
"""
Real Provider Testing Script

This script helps you test the UniLLM API Gateway with real API keys
and experiment with different providers and models.
"""

import os
import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "test-client-key"  # This can be any string for now

def setup_environment():
    """Set up environment variables from .env file."""
    print("🔧 Setting up environment...")
    
    # Load from .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                    print(f"✅ Loaded {key}")
    else:
        print("⚠️  No .env file found. Please create one with your API keys.")
    
    print()

def make_chat_request(model: str, messages: List[Dict[str, str]], **kwargs) -> Optional[Dict]:
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
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

def test_provider_connectivity():
    """Test which providers are working with your API keys."""
    
    print("🔍 === Testing Provider Connectivity ===")
    
    # Test models from different providers
    test_models = [
        ("gpt-3.5-turbo", "OpenAI"),
        ("gpt-4", "OpenAI"),
        ("claude-3-sonnet", "Anthropic"),
        ("claude-3-haiku", "Anthropic"),
        ("gemini-pro", "Google Gemini"),
    ]
    
    working_providers = []
    
    for model, provider_name in test_models:
        print(f"\n🤖 Testing {provider_name} ({model})...")
        
        response = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": "Say 'Hello' if you can hear me."}],
            max_tokens=50
        )
        
        if response:
            print(f"✅ {provider_name} is working!")
            print(f"   Response: {response['content']}")
            print(f"   Provider: {response['provider']}")
            print(f"   Tokens: {response['usage']['total_tokens']}")
            working_providers.append(provider_name)
        else:
            print(f"❌ {provider_name} is not working (check API key)")
    
    print(f"\n📊 Summary: {len(working_providers)}/{len(test_models)} providers working")
    if working_providers:
        print(f"✅ Working providers: {', '.join(set(working_providers))}")
    
    return working_providers

def test_provider_switching():
    """Test switching between different providers with the same question."""
    
    print("\n🔄 === Provider Switching Test ===")
    
    question = "What is the capital of France and why is it famous?"
    
    # Test with working providers
    models_to_test = [
        ("gpt-3.5-turbo", "OpenAI GPT-3.5"),
        ("gpt-4", "OpenAI GPT-4"),
        ("claude-3-sonnet", "Anthropic Claude-3-Sonnet"),
        ("claude-3-haiku", "Anthropic Claude-3-Haiku"),
        ("gemini-pro", "Google Gemini Pro"),
    ]
    
    responses = {}
    
    for model, name in models_to_test:
        print(f"\n🤖 Testing {name}...")
        
        response = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": question}],
            max_tokens=200,
            temperature=0.7
        )
        
        if response:
            responses[model] = response
            print(f"✅ Got response ({response['usage']['total_tokens']} tokens)")
        else:
            print(f"❌ Failed to get response")
    
    # Compare responses
    print("\n" + "="*80)
    print("📊 RESPONSE COMPARISON")
    print("="*80)
    
    for model, name in models_to_test:
        if model in responses:
            resp = responses[model]
            print(f"\n🔹 {name}:")
            print(f"   Content: {resp['content'][:150]}...")
            print(f"   Tokens: {resp['usage']['total_tokens']}")
            print(f"   Provider: {resp['provider']}")
            print(f"   Finish Reason: {resp['finish_reason']}")

def test_conversation_switching():
    """Test switching providers mid-conversation."""
    
    print("\n🗣️ === Conversation Provider Switching Test ===")
    
    # Start a conversation
    conversation = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": "I want to visit Paris. What should I know?"}
    ]
    
    # Get initial response from OpenAI
    print("\n🗣️ Starting conversation with OpenAI (GPT-3.5)...")
    response1 = make_chat_request(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=150
    )
    
    if response1:
        print(f"✅ OpenAI Response: {response1['content'][:100]}...")
        
        # Add OpenAI's response to conversation
        conversation.append({"role": "assistant", "content": response1['content']})
        conversation.append({"role": "user", "content": "What about the best time to visit?"})
        
        # Continue with Anthropic
        print("\n🔄 Switching to Anthropic (Claude-3-Sonnet)...")
        response2 = make_chat_request(
            model="claude-3-sonnet",
            messages=conversation,
            max_tokens=150
        )
        
        if response2:
            print(f"✅ Anthropic Response: {response2['content'][:100]}...")
            
            # Continue with Gemini
            conversation.append({"role": "assistant", "content": response2['content']})
            conversation.append({"role": "user", "content": "What about transportation options?"})
            
            print("\n🔄 Switching to Google Gemini...")
            response3 = make_chat_request(
                model="gemini-pro",
                messages=conversation,
                max_tokens=150
            )
            
            if response3:
                print(f"✅ Gemini Response: {response3['content'][:100]}...")
            else:
                print("❌ Failed to get response from Gemini")
        else:
            print("❌ Failed to get response from Anthropic")
    else:
        print("❌ Failed to get response from OpenAI")

def test_different_parameters():
    """Test different parameters with the same model."""
    
    print("\n🎛️ === Parameter Testing ===")
    
    question = "Write a creative story about a robot"
    model = "gpt-3.5-turbo"  # Use a reliable model
    
    # Test different temperatures
    temperatures = [0.1, 0.7, 1.0]
    
    for temp in temperatures:
        print(f"\n🌡️ Testing temperature {temp}...")
        
        response = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": question}],
            temperature=temp,
            max_tokens=100
        )
        
        if response:
            print(f"✅ Response: {response['content'][:80]}...")
        else:
            print(f"❌ Failed to get response")

def test_model_capabilities():
    """Test different capabilities of various models."""
    
    print("\n🧠 === Model Capabilities Test ===")
    
    test_prompts = [
        ("What is 2+2?", "Basic math"),
        ("Explain quantum computing in simple terms", "Complex explanation"),
        ("Write a haiku about technology", "Creative writing"),
        ("What are the three laws of robotics?", "Knowledge retrieval"),
    ]
    
    models = ["gpt-3.5-turbo", "claude-3-sonnet", "gemini-pro"]
    
    for prompt, description in test_prompts:
        print(f"\n📝 Testing: {description}")
        print(f"Prompt: {prompt}")
        
        for model in models:
            print(f"\n🤖 {model}:")
            
            response = make_chat_request(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            
            if response:
                print(f"   {response['content'][:80]}...")
            else:
                print(f"   ❌ Failed")

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
    
    print("🚀 UniLLM API Gateway - Real Provider Testing")
    print("=" * 60)
    
    # Set up environment
    setup_environment()
    
    # Check if API is running
    if not check_api_status():
        print("\nTo start the API gateway, run:")
        print("python main.py")
        return
    
    print("\n" + "="*60)
    
    # Run tests
    working_providers = test_provider_connectivity()
    
    if working_providers:
        test_provider_switching()
        test_conversation_switching()
        test_different_parameters()
        test_model_capabilities()
    else:
        print("\n❌ No providers are working. Please check your API keys in the .env file.")
        print("\nRequired API keys:")
        print("- OPENAI_API_KEY")
        print("- ANTHROPIC_API_KEY") 
        print("- GEMINI_API_KEY")
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main() 