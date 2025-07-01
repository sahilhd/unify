"""
Basic usage example for UniLLM library.
"""

from unillm import ChatLLM

def main():
    # Set your API key (you would get this from your UniLLM dashboard)
    ChatLLM.api_key = "your-unillm-api-key"
    
    # Example 1: Basic chat with GPT-4
    print("=== Example 1: Basic chat with GPT-4 ===")
    response = ChatLLM.chat(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    print(f"Response: {response.content}")
    print(f"Model: {response.model}")
    print(f"Provider: {response.provider}")
    print(f"Tokens used: {response.usage.total_tokens}")
    print()
    
    # Example 2: Chat with Claude
    print("=== Example 2: Chat with Claude ===")
    response = ChatLLM.chat(
        model="claude-3-sonnet",
        messages=[
            {"role": "user", "content": "Explain quantum computing in simple terms"}
        ]
    )
    print(f"Response: {response.content}")
    print(f"Model: {response.model}")
    print(f"Provider: {response.provider}")
    print()
    
    # Example 3: Conversation with system message
    print("=== Example 3: Conversation with system message ===")
    response = ChatLLM.chat(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers"}
        ],
        temperature=0.7
    )
    print(f"Response: {response.content}")
    print()
    
    # Example 4: Streaming response
    print("=== Example 4: Streaming response ===")
    print("Generating story with streaming...")
    for chunk in ChatLLM.chat(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Write a short story about a robot learning to paint"}
        ],
        stream=True,
        max_tokens=200
    ):
        print(chunk.content, end="", flush=True)
    print("\n")
    
    # Example 5: List available models
    print("=== Example 5: Available models ===")
    models = ChatLLM.list_models()
    print(f"Total models available: {len(models)}")
    print("First 10 models:", models[:10])
    print()
    
    # Example 6: Get model information
    print("=== Example 6: Model information ===")
    model_info = ChatLLM.get_model_info("gpt-4")
    if model_info:
        print(f"Model: {model_info['model']}")
        print(f"Provider: {model_info['provider']}")

if __name__ == "__main__":
    main() 