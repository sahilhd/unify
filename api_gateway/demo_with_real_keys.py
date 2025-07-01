#!/usr/bin/env python3
"""
Demo script showing how to use the UniLLM API Gateway with real API keys.

This script demonstrates:
1. Setting up API keys
2. Making requests to different providers
3. Switching between providers seamlessly
4. Continuing conversations across providers
"""

import os
import requests
import json
from typing import Dict, List

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "your-unillm-api-key"  # This can be any string for authentication

def setup_environment():
    """Set up environment variables for API keys."""
    print("🔧 Setting up environment variables...")
    
    # You would set these in your .env file or environment
    api_keys = {
        "OPENAI_API_KEY": "your-openai-api-key-here",
        "ANTHROPIC_API_KEY": "your-anthropic-api-key-here", 
        "GEMINI_API_KEY": "your-gemini-api-key-here",
        "MISTRAL_API_KEY": "your-mistral-api-key-here",
        "COHERE_API_KEY": "your-cohere-api-key-here"
    }
    
    # Set environment variables (for demo purposes)
    for key, value in api_keys.items():
        if value != f"your-{key.lower().replace('_', '-')}-here":
            os.environ[key] = value
            print(f"✅ Set {key}")
        else:
            print(f"⚠️  {key} not configured (using placeholder)")
    
    print()

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
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

def demo_basic_provider_switching():
    """Demonstrate basic provider switching."""
    
    print("🔄 === Basic Provider Switching Demo ===")
    
    question = "What is the capital of France and why is it famous?"
    
    # Test different providers
    providers = [
        ("gpt-4", "OpenAI GPT-4"),
        ("claude-3-sonnet", "Anthropic Claude-3-Sonnet"),
        ("gemini-pro", "Google Gemini Pro"),
    ]
    
    for model, name in providers:
        print(f"\n🤖 Testing {name}...")
        
        response = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": question}],
            max_tokens=150,
            temperature=0.7
        )
        
        if response:
            print(f"✅ {name} Response:")
            print(f"   Content: {response['content'][:100]}...")
            print(f"   Provider: {response['provider']}")
            print(f"   Tokens: {response['usage']['total_tokens']}")
        else:
            print(f"❌ Failed to get response from {name}")
    
    print("\n" + "="*60)

def demo_conversation_switching():
    """Demonstrate switching providers mid-conversation."""
    
    print("🗣️ === Conversation Provider Switching Demo ===")
    
    # Start a conversation about travel
    conversation = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": "I want to visit Paris. What should I know?"}
    ]
    
    # Get initial response from OpenAI
    print("\n🗣️ Starting conversation with OpenAI (GPT-4)...")
    response1 = make_chat_request(
        model="gpt-4",
        messages=conversation,
        max_tokens=200
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
            max_tokens=200
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
                max_tokens=200
            )
            
            if response3:
                print(f"✅ Gemini Response: {response3['content'][:100]}...")
            else:
                print("❌ Failed to get response from Gemini")
        else:
            print("❌ Failed to get response from Anthropic")
    else:
        print("❌ Failed to get response from OpenAI")
    
    print("\n" + "="*60)

def demo_model_comparison():
    """Compare responses from different models for the same question."""
    
    print("📊 === Model Comparison Demo ===")
    
    question = "Explain quantum computing in simple terms"
    
    models = [
        ("gpt-4", "OpenAI GPT-4"),
        ("claude-3-sonnet", "Anthropic Claude-3-Sonnet"),
        ("gemini-pro", "Google Gemini Pro"),
    ]
    
    responses = {}
    
    for model, name in models:
        print(f"\n🤖 Getting response from {name}...")
        
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
    
    print("\n" + "="*60)
    print("📊 COMPARISON RESULTS")
    print("="*60)
    
    for model, name in models:
        if model in responses:
            resp = responses[model]
            print(f"\n🔹 {name}:")
            print(f"   Content: {resp['content'][:150]}...")
            print(f"   Tokens: {resp['usage']['total_tokens']}")
            print(f"   Provider: {resp['provider']}")
    
    print("\n" + "="*60)

def demo_advanced_features():
    """Demonstrate advanced features like streaming and different parameters."""
    
    print("🚀 === Advanced Features Demo ===")
    
    # Test different temperature settings
    print("\n🌡️ Testing different temperature settings...")
    
    temperatures = [0.1, 0.7, 1.0]
    question = "Write a creative story about a robot"
    
    for temp in temperatures:
        print(f"\n🤖 Testing temperature {temp}...")
        
        response = make_chat_request(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            temperature=temp,
            max_tokens=100
        )
        
        if response:
            print(f"✅ Response (temp {temp}): {response['content'][:80]}...")
        else:
            print(f"❌ Failed to get response")
    
    # Test different models with same prompt
    print("\n🎯 Testing different models with same prompt...")
    
    prompt = "What are the three laws of robotics?"
    models = ["gpt-4", "claude-3-sonnet", "gemini-pro"]
    
    for model in models:
        print(f"\n🤖 Testing {model}...")
        
        response = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        if response:
            print(f"✅ {model}: {response['content'][:100]}...")
        else:
            print(f"❌ Failed to get response from {model}")
    
    print("\n" + "="*60)

def main():
    """Main function to run all demos."""
    
    print("🚀 UniLLM API Gateway - Real API Keys Demo")
    print("=" * 60)
    
    # Set up environment
    setup_environment()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API Gateway is running")
        else:
            print("❌ API Gateway is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API Gateway. Make sure it's running on http://localhost:8000")
        return
    
    print("\n" + "="*60)
    
    # Run demos
    demo_basic_provider_switching()
    demo_conversation_switching()
    demo_model_comparison()
    demo_advanced_features()
    
    print("\n🎉 Demo completed!")
    print("\n💡 To use with real API keys:")
    print("1. Edit your .env file with actual API keys")
    print("2. Restart the API gateway")
    print("3. Run this script again")

if __name__ == "__main__":
    main() 