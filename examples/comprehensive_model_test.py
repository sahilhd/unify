#!/usr/bin/env python3
"""
Comprehensive test for ALL models in the UniLLM registry.
Tests every single model to ensure they work with the same code pattern.
"""

from unillm import UniLLM
from unillm.registry import model_registry
import time

def test_all_models():
    """Test every single model in the registry."""
    
    # Initialize client with automatic SaaS URL
    client = UniLLM(api_key="unillm_yL5miUBRVH3qwVrMPCYfJ8u8dicMJ96x")
    
    print("🚀 Comprehensive Model Test - UniLLM v0.1.5")
    print("=" * 60)
    print(f"✅ Client initialized with base_url: {client.base_url}")
    print()
    
    # Get all models from registry
    all_models = model_registry.list_models()
    all_models.sort()  # Sort for consistent output
    
    print(f"📋 Testing {len(all_models)} models:")
    print("-" * 60)
    
    # Test results tracking
    successful_models = []
    failed_models = []
    
    # Test each model
    for i, model in enumerate(all_models, 1):
        print(f"\n{i:2d}/{len(all_models)} 🧪 Testing: {model}")
        
        try:
            # Same code works with any provider!
            response = client.chat(
                model=model,
                messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
            )
            
            print(f"   ✅ SUCCESS: {model}")
            print(f"      Response: {response.content[:100]}{'...' if len(response.content) > 100 else ''}")
            print(f"      Model used: {response.model}")
            print(f"      Provider: {model_registry.get_provider(model)}")
            
            successful_models.append(model)
            
        except Exception as e:
            print(f"   ❌ FAILED: {model}")
            print(f"      Error: {str(e)[:100]}{'...' if len(str(e)) > 100 else ''}")
            print(f"      Provider: {model_registry.get_provider(model)}")
            
            failed_models.append((model, str(e)))
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {len(successful_models)}/{len(all_models)} models")
    print(f"❌ Failed: {len(failed_models)}/{len(all_models)} models")
    print(f"📈 Success Rate: {(len(successful_models)/len(all_models)*100):.1f}%")
    
    # Provider breakdown
    print("\n📋 Provider Breakdown:")
    providers = {}
    for model in successful_models:
        provider = model_registry.get_provider(model)
        if provider not in providers:
            providers[provider] = []
        providers[provider].append(model)
    
    for provider, models in providers.items():
        print(f"   {provider}: {len(models)} models working")
    
    # Failed models details
    if failed_models:
        print(f"\n❌ Failed Models:")
        for model, error in failed_models:
            provider = model_registry.get_provider(model)
            print(f"   {model} ({provider}): {error}")
    
    # Working models by provider
    print(f"\n✅ Working Models by Provider:")
    for provider, models in providers.items():
        print(f"\n   {provider.upper()}:")
        for model in sorted(models):
            print(f"     - {model}")
    
    print(f"\n🎉 Test completed!")
    return successful_models, failed_models

def test_provider_specific():
    """Test models grouped by provider for better organization."""
    
    client = UniLLM(api_key="unillm_yL5miUBRVH3qwVrMPCYfJ8u8dicMJ96x")
    
    print("\n" + "=" * 60)
    print("🔍 PROVIDER-SPECIFIC TESTS")
    print("=" * 60)
    
    providers = ["openai", "anthropic", "gemini", "mistral", "cohere"]
    
    for provider in providers:
        print(f"\n🧪 Testing {provider.upper()} models:")
        print("-" * 40)
        
        models = model_registry.get_models_for_provider(provider)
        if not models:
            print(f"   No models found for {provider}")
            continue
        
        for model in sorted(models):
            try:
                response = client.chat(
                    model=model,
                    messages=[{"role": "user", "content": f"Hello from {provider}! What's 2+2?"}]
                )
                print(f"   ✅ {model}: {response.content[:50]}...")
            except Exception as e:
                print(f"   ❌ {model}: {str(e)[:50]}...")
            
            time.sleep(0.3)

if __name__ == "__main__":
    # Run comprehensive test
    successful, failed = test_all_models()
    
    # Run provider-specific test
    test_provider_specific()
    
    print(f"\n🎯 Final Result: {len(successful)}/{len(successful) + len(failed)} models working!") 