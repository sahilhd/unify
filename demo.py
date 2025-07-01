#!/usr/bin/env python3
"""
Demo script for UniLLM library.

This script demonstrates the library's capabilities without requiring real API keys.
It shows the interface and structure, but won't make actual API calls.
"""

from unillm import ChatLLM, ChatMessage, ChatResponse, TokenUsage
from datetime import datetime


def demo_basic_interface():
    """Demonstrate the basic interface."""
    print("=== UniLLM Library Demo ===\n")
    
    # Show available models
    print("1. Available Models:")
    models = ChatLLM.list_models()
    print(f"   Total models: {len(models)}")
    print(f"   Sample models: {', '.join(models[:5])}...")
    print()
    
    # Show available providers
    print("2. Available Providers:")
    providers = ChatLLM.list_providers()
    for provider in providers:
        provider_models = [m for m in models if ChatLLM.get_model_info(m)["provider"] == provider]
        print(f"   {provider.capitalize()}: {len(provider_models)} models")
    print()
    
    # Show model information
    print("3. Model Information:")
    sample_models = ["gpt-4", "claude-3-sonnet", "gemini-pro", "mistral-large"]
    for model in sample_models:
        info = ChatLLM.get_model_info(model)
        if info:
            print(f"   {model} -> {info['provider']}")
    print()


def demo_message_creation():
    """Demonstrate message creation."""
    print("4. Message Creation:")
    
    # Create messages using dictionaries
    messages_dict = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2 + 2?"}
    ]
    print(f"   Messages from dict: {len(messages_dict)} messages")
    
    # Create messages using ChatMessage objects
    messages_objects = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="What is 2 + 2?")
    ]
    print(f"   Messages from objects: {len(messages_objects)} messages")
    print()


def demo_response_structure():
    """Demonstrate response structure."""
    print("5. Response Structure:")
    
    # Create a mock response
    usage = TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    response = ChatResponse(
        content="2 + 2 equals 4.",
        model="gpt-4",
        provider="openai",
        usage=usage,
        finish_reason="stop",
        created_at=datetime.now()
    )
    
    print(f"   Content: {response.content}")
    print(f"   Model: {response.model}")
    print(f"   Provider: {response.provider}")
    print(f"   Tokens used: {response.usage.total_tokens}")
    print(f"   Finish reason: {response.finish_reason}")
    print()


def demo_interface_examples():
    """Show interface examples."""
    print("6. Interface Examples:")
    print("   # Basic usage:")
    print("   ChatLLM.api_key = 'your-api-key'")
    print("   response = ChatLLM.chat(")
    print("       model='gpt-4',")
    print("       messages=[{'role': 'user', 'content': 'Hello'}]")
    print("   )")
    print()
    
    print("   # With parameters:")
    print("   response = ChatLLM.chat(")
    print("       model='claude-3-sonnet',")
    print("       messages=[{'role': 'user', 'content': 'Explain quantum computing'}],")
    print("       temperature=0.7,")
    print("       max_tokens=500")
    print("   )")
    print()
    
    print("   # Streaming:")
    print("   for chunk in ChatLLM.chat(")
    print("       model='gpt-4',")
    print("       messages=[{'role': 'user', 'content': 'Write a story'}],")
    print("       stream=True")
    print("   ):")
    print("       print(chunk.content, end='')")
    print()


def demo_error_handling():
    """Demonstrate error handling."""
    print("7. Error Handling:")
    print("   try:")
    print("       response = ChatLLM.chat(")
    print("           model='non-existent-model',")
    print("           messages=[{'role': 'user', 'content': 'Hello'}]")
    print("       )")
    print("   except ModelNotFoundError as e:")
    print("       print(f'Model not found: {e.message}')")
    print()
    
    print("   try:")
    print("       response = ChatLLM.chat(")
    print("           model='gpt-4',")
    print("           messages=[{'role': 'user', 'content': 'Hello'}],")
    print("           temperature=3.0  # Invalid temperature")
    print("       )")
    print("   except ValueError as e:")
    print("       print(f'Validation error: {e}')")
    print()


def demo_configuration():
    """Demonstrate configuration options."""
    print("8. Configuration Options:")
    print("   # Method 1: Direct assignment")
    print("   ChatLLM.api_key = 'your-api-key'")
    print("   ChatLLM.base_url = 'https://api.unillm.com'")
    print("   ChatLLM.timeout = 60")
    print()
    
    print("   # Method 2: Configure method")
    print("   ChatLLM.configure(")
    print("       api_key='your-api-key',")
    print("       base_url='https://api.unillm.com',")
    print("       timeout=60")
    print("   )")
    print()
    
    print("   # Method 3: Environment variables")
    print("   export UNILLM_API_KEY='your-api-key'")
    print("   export UNILLM_BASE_URL='https://api.unillm.com'")
    print("   export UNILLM_TIMEOUT='60'")
    print()


def main():
    """Run the demo."""
    demo_basic_interface()
    demo_message_creation()
    demo_response_structure()
    demo_interface_examples()
    demo_error_handling()
    demo_configuration()
    
    print("=== Demo Complete ===")
    print("\nTo use the library with real API calls:")
    print("1. Get an API key from your UniLLM dashboard")
    print("2. Set ChatLLM.api_key = 'your-api-key'")
    print("3. Start making requests!")
    print("\nFor more examples, see the 'examples/' directory.")


if __name__ == "__main__":
    main() 