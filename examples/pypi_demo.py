#!/usr/bin/env python3
"""
PyPI Demo: Using the UniLLM PyPI library

This demo shows how to use the UniLLM library from PyPI.
First, install it with: pip install unifyllm-sdk
"""

import os
import sys
import json
from datetime import datetime

# Import from PyPI library
from unillm import UniLLM
from unillm.models import ChatMessage

def test_providers():
    """Test all available providers."""
    
    # Initialize client (no base_url needed for SaaS)
    client = UniLLM(
        api_key="your_api_key_here"  # Replace with your actual API key
    )
    
    print("🚀 UniLLM PyPI Demo")
    print("=" * 50)
    
    # Test prompts for each provider
    tests = [
        {
            "name": "Claude (Anthropic)",
            "model": "claude-3-sonnet",
            "prompt": "Explain quantum computing in simple terms."
        },
        {
            "name": "GPT-4 (OpenAI)", 
            "model": "gpt-4o",
            "prompt": "Write a short poem about artificial intelligence."
        },
        {
            "name": "Gemini (Google)",
            "model": "gemini-1.5-flash", 
            "prompt": "Summarize the benefits of renewable energy in 3 points."
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\n🧪 Testing {test['name']}...")
        
        try:
            response = client.chat(
                model=test["model"],
                messages=[ChatMessage(role="user", content=test["prompt"])],
                temperature=0.7,
                max_tokens=200
            )
            
            print(f"✅ {test['name']} working!")
            print(f"   Response: {response.content[:100]}...")
            print(f"   Tokens: {response.usage.total_tokens}")
            
            results.append({
                "provider": test["name"],
                "model": test["model"],
                "success": True,
                "response": response.content,
                "tokens": response.usage.total_tokens
            })
            
        except Exception as e:
            print(f"❌ {test['name']} failed: {e}")
            results.append({
                "provider": test["name"],
                "model": test["model"],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RESULTS SUMMARY")
    print("=" * 50)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{result['provider']:20} {status}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pypi_demo_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")
    
    # Check if all passed
    all_passed = all(r["success"] for r in results)
    
    if all_passed:
        print("\n🎉 All providers working! Your PyPI setup is complete.")
    else:
        print("\n⚠️  Some providers failed. Check the results file for details.")

if __name__ == "__main__":
    # Check if API key is set
    if "your_api_key_here" in open(__file__).read():
        print("⚠️  Please update the API key in the script before running!")
        print("   Replace 'your_api_key_here' with your actual UniLLM API key.")
        sys.exit(1)
    
    test_providers() 