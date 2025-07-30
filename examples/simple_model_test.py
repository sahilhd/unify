#!/usr/bin/env python3
"""
Simple test showing the basic pattern for each model.
Demonstrates that the same code works with any provider!
"""

from unillm import UniLLM
from unillm.registry import model_registry

def test_basic_pattern():
    """Test the basic pattern with a few models from each provider."""
    
    # Initialize client with automatic SaaS URL
    client = UniLLM(api_key="unillm_yL5miUBRVH3qwVrMPCYfJ8u8dicMJ96x")
    
    print("🚀 Simple Model Test - Same Code Works with Any Provider!")
    print("=" * 65)
    
    # Test models from each provider
    test_models = [
        # OpenAI models
        "gpt-4o",
        "gpt-4o-mini", 
        "gpt-3.5-turbo",
        
        # Anthropic models
        "claude-3-sonnet",
        "claude-3-haiku",
        "claude-3-opus",
        
        # Gemini models
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash",
        
        # Mistral models
        "mistral-large",
        "mistral-medium",
        "mistral-small",
        
        # Cohere models
        "command",
        "command-light",
    ]
    
    for model in test_models:
        print(f"\n🧪 Testing: {model}")
        print(f"   Provider: {model_registry.get_provider(model)}")
        
        try:
            # Same code works with any provider!
            response = client.chat(
                model=model,
                messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
            )
            
            print(f"   ✅ SUCCESS!")
            print(f"   Response: {response.content}")
            print(f"   Model used: {response.model}")
            
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}")
        
        print("-" * 50)

def show_all_available_models():
    """Show all available models in the registry."""
    
    print("\n📋 ALL AVAILABLE MODELS:")
    print("=" * 50)
    
    all_models = model_registry.list_models()
    all_models.sort()
    
    providers = {}
    for model in all_models:
        provider = model_registry.get_provider(model)
        if provider not in providers:
            providers[provider] = []
        providers[provider].append(model)
    
    for provider, models in providers.items():
        print(f"\n{provider.upper()}:")
        for model in sorted(models):
            print(f"  - {model}")
    
    print(f"\nTotal: {len(all_models)} models across {len(providers)} providers")

if __name__ == "__main__":
    # Show available models
    show_all_available_models()
    
    # Test basic pattern
    test_basic_pattern()
    
    print("\n🎉 Test completed!")
    print("\n💡 Key Takeaway: The same code works with any provider!")
    print("   Just change the model name and everything else stays the same!") 