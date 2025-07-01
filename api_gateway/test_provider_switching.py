#!/usr/bin/env python3
"""
Test script to demonstrate switching between different LLM providers.

This script shows how to use the UniLLM API Gateway to get responses
from different providers using the same interface.
"""

import requests
import json
from typing import Dict, List

# API Gateway configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "your-unillm-api-key"  # This can be any string for now

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
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
    return response.json()

def test_provider_switching():
    """Test switching between different providers."""
    
    print("=== UniLLM Provider Switching Demo ===\n")
    
    # Test question
    question = "What is the capital of France and why is it famous?"
    
    # Models to test (from different providers)
    models_to_test = [
        ("gpt-4", "OpenAI"),
        ("claude-3-sonnet", "Anthropic"),
        ("gemini-pro", "Google Gemini"),
    ]
    
    for model, provider_name in models_to_test:
        print(f"🤖 Testing {provider_name} ({model})")
        print(f"Question: {question}")
        print("-" * 50)
        
        try:
            response = make_chat_request(
                model=model,
                messages=[{"role": "user", "content": question}],
                max_tokens=150,
                temperature=0.7
            )
            
            if response:
                print(f"✅ Response from {provider_name}:")
                print(f"Content: {response['content']}")
                print(f"Provider: {response['provider']}")
                print(f"Tokens used: {response['usage']['total_tokens']}")
                print(f"Finish reason: {response['finish_reason']}")
            else:
                print(f"❌ Failed to get response from {provider_name}")
                
        except Exception as e:
            print(f"❌ Error with {provider_name}: {str(e)}")
        
        print("\n" + "="*60 + "\n")

def test_conversation_switching():
    """Test switching providers mid-conversation."""
    
    print("=== Conversation Provider Switching Demo ===\n")
    
    # Start a conversation
    conversation = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": "I want to visit Paris. What should I know?"}
    ]
    
    # Get initial response from OpenAI
    print("🗣️ Starting conversation with OpenAI (GPT-4)...")
    response1 = make_chat_request(
        model="gpt-4",
        messages=conversation,
        max_tokens=200
    )
    
    if response1:
        print(f"OpenAI Response: {response1['content'][:100]}...")
        
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
            print(f"Anthropic Response: {response2['content'][:100]}...")
            
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
                print(f"Gemini Response: {response3['content'][:100]}...")
            else:
                print("❌ Failed to get response from Gemini")
        else:
            print("❌ Failed to get response from Anthropic")
    else:
        print("❌ Failed to get response from OpenAI")

def test_model_comparison():
    """Compare responses from different models for the same question."""
    
    print("=== Model Comparison Demo ===\n")
    
    question = "Explain quantum computing in simple terms"
    
    models = [
        ("gpt-4", "OpenAI GPT-4"),
        ("claude-3-sonnet", "Anthropic Claude-3-Sonnet"),
        ("gemini-pro", "Google Gemini Pro"),
    ]
    
    responses = {}
    
    for model, name in models:
        print(f"🤖 Getting response from {name}...")
        
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
    
    print("🚀 UniLLM API Gateway Testing")
    print("=" * 50)
    
    # Check if API is running
    if not check_api_status():
        print("\nTo start the API gateway, run:")
        print("cd api_gateway")
        print("python main.py")
        return
    
    print("\n" + "="*50)
    
    # Run tests
    test_provider_switching()
    
    print("\n" + "="*50)
    test_conversation_switching()
    
    print("\n" + "="*50)
    test_model_comparison()
    
    print("\n🎉 Demo completed!")

if __name__ == "__main__":
    main() 