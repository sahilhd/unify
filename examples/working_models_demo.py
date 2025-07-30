#!/usr/bin/env python3
"""
Demo showing the same code works with any provider!
Only tests models that are confirmed to work.
"""

from unillm import UniLLM

def demo_unified_interface():
    """Demonstrate that the same code works with any provider."""
    
    # Initialize client with automatic SaaS URL
    client = UniLLM(api_key="unillm_yL5miUBRVH3qwVrMPCYfJ8u8dicMJ96x")
    
    print("🚀 UniLLM Demo - Same Code Works with Any Provider!")
    print("=" * 55)
    print("💡 The exact same code works with OpenAI, Anthropic, and Gemini!")
    print()
    
    # Test models that are confirmed to work
    working_models = [
        # OpenAI models
        ("gpt-4o", "OpenAI"),
        ("gpt-4o-mini", "OpenAI"), 
        ("gpt-3.5-turbo", "OpenAI"),
        
        # Anthropic models
        ("claude-3-sonnet", "Anthropic"),
        ("claude-3-haiku", "Anthropic"),
        ("claude-3-opus", "Anthropic"),
        
        # Gemini models
        ("gemini-1.5-flash", "Google Gemini"),
        ("gemini-2.0-flash", "Google Gemini"),
    ]
    
    for model, provider in working_models:
        print(f"🧪 Testing {provider} model: {model}")
        
        # Same code works with any provider!
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
        )
        
        print(f"   ✅ Response: {response.content}")
        print(f"   📝 Model used: {response.model}")
        print("-" * 50)

def show_code_pattern():
    """Show the simple code pattern."""
    
    print("\n💻 CODE PATTERN:")
    print("=" * 30)
    print("""
from unillm import UniLLM

# Initialize once
client = UniLLM(api_key="your_api_key")

# Same code works with any provider!
response = client.chat(
    model="gpt-4o",  # OpenAI
    messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
)
print(response.content)

# Switch to Anthropic with the same code
response = client.chat(
    model="claude-3-sonnet",  # Anthropic
    messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
)
print(response.content)

# Switch to Gemini with the same code
response = client.chat(
    model="gemini-1.5-flash",  # Google Gemini
    messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
)
print(response.content)
""")

def show_available_models():
    """Show all available models."""
    
    print("\n📋 AVAILABLE MODELS:")
    print("=" * 25)
    
    models_by_provider = {
        "OpenAI": [
            "gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-4-turbo",
            "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
        ],
        "Anthropic": [
            "claude-3-sonnet", "claude-3-haiku", "claude-3-opus",
            "claude-3-5-sonnet-20241022", "claude-3-7-sonnet-20250219"
        ],
        "Google Gemini": [
            "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash",
            "gemini-2.5-flash", "gemini-2.5-pro"
        ],
        "Mistral": [
            "mistral-large", "mistral-medium", "mistral-small"
        ],
        "Cohere": [
            "command", "command-light"
        ]
    }
    
    for provider, models in models_by_provider.items():
        print(f"\n{provider}:")
        for model in models:
            print(f"  - {model}")

if __name__ == "__main__":
    # Show the demo
    demo_unified_interface()
    
    # Show code pattern
    show_code_pattern()
    
    # Show available models
    show_available_models()
    
    print("\n🎉 Demo completed!")
    print("\n✨ Key Benefits:")
    print("   • Single API key for all providers")
    print("   • Same code works with any model")
    print("   • Easy to switch between providers")
    print("   • No need to manage multiple API keys")
    print("   • Automatic SaaS backend (no setup required)") 