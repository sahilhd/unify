#!/usr/bin/env python3
"""
Simple example of using the UniLLM client library.

This example shows how to use the UniLLM client to chat with different models
through your UniLLM API gateway.
"""

import os
from unillm import UniLLM, chat

def main():
    # Method 1: Using the client class
    print("=== Using UniLLM Client Class ===")
    
    # Initialize client with your API key
    # You can either pass it directly or set UNILLM_API_KEY environment variable
    api_key = "your-unillm-api-key-here"  # Replace with your actual API key
    client = UniLLM(api_key=api_key)
    
    # Check if the API is healthy
    if client.health_check():
        print("✅ API is healthy!")
    else:
        print("❌ API is not responding")
        return
    
    # Send a simple message
    messages = [
        {"role": "user", "content": "Hello! What's 2+2?"}
    ]
    
    try:
        response = client.chat(
            model="gpt-4",  # or "claude-3-sonnet", "gemini-pro", etc.
            messages=messages,
            temperature=0.7
        )
        
        print(f"🤖 Response: {response.content}")
        print(f"📊 Model used: {response.model}")
        print(f"📈 Usage: {response.usage}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 2: Using the convenience function
    print("=== Using Convenience Function ===")
    
    try:
        # Set your API key as environment variable
        os.environ["UNILLM_API_KEY"] = api_key
        
        response = chat(
            model="gpt-4",
            messages=[{"role": "user", "content": "Tell me a short joke"}],
            temperature=0.8
        )
        
        print(f"🤖 Response: {response.content}")
        print(f"📊 Model used: {response.model}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 3: Conversation example
    print("=== Conversation Example ===")
    
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "My name is Alice. Remember this."},
        {"role": "assistant", "content": "Hello Alice! I'll remember your name."},
        {"role": "user", "content": "What's my name?"}
    ]
    
    try:
        response = client.chat(
            model="gpt-4",
            messages=conversation
        )
        
        print(f"🤖 Response: {response.content}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 