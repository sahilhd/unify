"""
Advanced usage example for UniLLM library.
"""

import os
from unillm import ChatLLM, UniLLMError, ModelNotFoundError

def error_handling_example():
    """Demonstrate error handling."""
    print("=== Error Handling Examples ===")
    
    # Example 1: Model not found
    try:
        response = ChatLLM.chat(
            model="non-existent-model",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except ModelNotFoundError as e:
        print(f"Model not found error: {e.message}")
    
    # Example 2: Invalid API key
    try:
        ChatLLM.api_key = "invalid-key"
        response = ChatLLM.chat(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except UniLLMError as e:
        print(f"API error: {e.message}")
        print(f"Provider: {e.provider}")
        print(f"Status code: {e.status_code}")

def configuration_example():
    """Demonstrate different configuration methods."""
    print("\n=== Configuration Examples ===")
    
    # Method 1: Direct assignment
    ChatLLM.api_key = "your-api-key"
    ChatLLM.base_url = "https://api.unillm.com"
    ChatLLM.timeout = 60
    
    # Method 2: Using configure method
    ChatLLM.configure(
        api_key="your-api-key",
        base_url="https://api.unillm.com",
        timeout=60
    )
    
    # Method 3: Environment variables
    os.environ["UNILLM_API_KEY"] = "your-api-key"
    os.environ["UNILLM_BASE_URL"] = "https://api.unillm.com"
    os.environ["UNILLM_TIMEOUT"] = "60"
    
    # Re-import to pick up environment variables
    import importlib
    import unillm
    importlib.reload(unillm)

def provider_comparison():
    """Compare responses from different providers."""
    print("\n=== Provider Comparison ===")
    
    ChatLLM.api_key = "your-api-key"
    
    question = "What is the meaning of life?"
    models_to_test = ["gpt-4", "claude-3-sonnet", "gemini-pro"]
    
    for model in models_to_test:
        try:
            print(f"\n--- {model.upper()} ---")
            response = ChatLLM.chat(
                model=model,
                messages=[{"role": "user", "content": question}],
                max_tokens=100
            )
            print(f"Response: {response.content}")
            print(f"Tokens: {response.usage.total_tokens}")
            print(f"Finish reason: {response.finish_reason}")
        except Exception as e:
            print(f"Error with {model}: {e}")

def conversation_example():
    """Demonstrate a multi-turn conversation."""
    print("\n=== Multi-turn Conversation ===")
    
    ChatLLM.api_key = "your-api-key"
    
    conversation = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": "I want to visit Paris. What should I know?"},
    ]
    
    # First turn
    response = ChatLLM.chat(
        model="gpt-4",
        messages=conversation
    )
    print(f"Assistant: {response.content}")
    
    # Add assistant's response to conversation
    conversation.append({"role": "assistant", "content": response.content})
    
    # Second turn
    conversation.append({"role": "user", "content": "What about the best time to visit?"})
    response = ChatLLM.chat(
        model="gpt-4",
        messages=conversation
    )
    print(f"Assistant: {response.content}")

def streaming_with_error_handling():
    """Demonstrate streaming with proper error handling."""
    print("\n=== Streaming with Error Handling ===")
    
    ChatLLM.api_key = "your-api-key"
    
    try:
        print("Generating response...")
        for chunk in ChatLLM.chat(
            model="gpt-4",
            messages=[{"role": "user", "content": "Write a poem about coding"}],
            stream=True,
            max_tokens=150
        ):
            print(chunk.content, end="", flush=True)
        print("\n")
    except UniLLMError as e:
        print(f"Streaming error: {e.message}")
    except KeyboardInterrupt:
        print("\nStreaming interrupted by user")

def model_discovery():
    """Demonstrate model discovery features."""
    print("\n=== Model Discovery ===")
    
    # List all providers
    providers = ChatLLM.list_providers()
    print(f"Available providers: {providers}")
    
    # List models for each provider
    for provider in providers:
        models = ChatLLM.list_models()
        provider_models = [m for m in models if ChatLLM.get_model_info(m)["provider"] == provider]
        print(f"\n{provider.upper()} models ({len(provider_models)}):")
        for model in provider_models[:5]:  # Show first 5
            print(f"  - {model}")
        if len(provider_models) > 5:
            print(f"  ... and {len(provider_models) - 5} more")

def main():
    """Run all advanced examples."""
    print("UniLLM Advanced Usage Examples")
    print("=" * 50)
    
    # Note: These examples require a valid API key to work
    print("Note: These examples require a valid UniLLM API key to work properly.")
    print("Replace 'your-api-key' with your actual API key.\n")
    
    # Uncomment the examples you want to run:
    
    # error_handling_example()
    # configuration_example()
    # provider_comparison()
    # conversation_example()
    # streaming_with_error_handling()
    # model_discovery()
    
    print("Examples completed. Uncomment the function calls above to run specific examples.")

if __name__ == "__main__":
    main() 