#!/usr/bin/env python3
"""
Interactive Testing Script

A simple interactive script to manually test different models and providers.
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

def make_request(model: str, message: str, **kwargs) -> Dict:
    """Make a chat request."""
    
    url = f"{API_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
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

def list_models():
    """List available models."""
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        if response.status_code == 200:
            data = response.json()
            print("\n📋 Available Models:")
            for model in data['models']:
                provider = data['model_provider_map'].get(model, 'Unknown')
                print(f"  - {model} ({provider})")
        else:
            print("❌ Failed to get models")
    except Exception as e:
        print(f"❌ Error: {e}")

def interactive_chat():
    """Interactive chat mode."""
    
    print("\n🤖 Interactive Chat Mode")
    print("Type 'quit' to exit, 'models' to see available models")
    print("Format: model:message (e.g., gpt-4:Hello)")
    
    conversation = []
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'models':
                list_models()
                continue
            elif user_input.lower() == 'clear':
                conversation = []
                print("🗑️ Conversation cleared")
                continue
            
            # Parse input
            if ':' in user_input:
                model, message = user_input.split(':', 1)
                model = model.strip()
                message = message.strip()
            else:
                # Default to GPT-3.5 if no model specified
                model = "gpt-3.5-turbo"
                message = user_input
            
            if not message:
                continue
            
            # Add to conversation
            conversation.append({"role": "user", "content": message})
            
            # Make request
            print(f"🤖 Requesting {model}...")
            
            response = make_request(
                model=model,
                message=message,
                max_tokens=500,
                temperature=0.7
            )
            
            if response:
                print(f"✅ {model} ({response['provider']}): {response['content']}")
                print(f"📊 Tokens: {response['usage']['total_tokens']}")
                
                # Add to conversation
                conversation.append({"role": "assistant", "content": response['content']})
            else:
                print(f"❌ Failed to get response from {model}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def quick_test():
    """Quick test with predefined prompts."""
    
    print("\n⚡ Quick Test Mode")
    
    test_cases = [
        ("gpt-3.5-turbo", "What is 2+2?"),
        ("gpt-4", "Explain quantum computing in one sentence"),
        ("claude-3-sonnet", "Write a haiku about AI"),
        ("claude-3-haiku", "What are the three laws of robotics?"),
        ("gemini-pro", "Tell me a joke about programming"),
    ]
    
    for model, prompt in test_cases:
        print(f"\n🤖 Testing {model}...")
        print(f"Prompt: {prompt}")
        
        response = make_request(
            model=model,
            message=prompt,
            max_tokens=100
        )
        
        if response:
            print(f"✅ Response: {response['content']}")
            print(f"📊 Provider: {response['provider']}, Tokens: {response['usage']['total_tokens']}")
        else:
            print(f"❌ Failed")

def main():
    """Main function."""
    
    print("🚀 UniLLM Interactive Testing")
    print("=" * 40)
    
    # Load environment
    load_env()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code != 200:
            print("❌ API Gateway is not running. Start it with: python main.py")
            return
        print("✅ API Gateway is running")
    except:
        print("❌ Cannot connect to API Gateway")
        return
    
    while True:
        print("\n" + "="*40)
        print("Choose an option:")
        print("1. Interactive Chat")
        print("2. Quick Test")
        print("3. List Models")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            interactive_chat()
        elif choice == '2':
            quick_test()
        elif choice == '3':
            list_models()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 