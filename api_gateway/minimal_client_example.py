#!/usr/bin/env python3
"""
Minimal UniLLM Client Example
Shows how simple it is to use UniLLM with minimal dependencies
"""

# Only need these imports - all standard or very common
import requests  # Usually pre-installed
import json      # Built into Python

def test_unillm_minimal():
    """Test UniLLM with minimal setup"""
    
    # Your API key (replace with actual key)
    API_KEY = "unillm_A4hEQGsyBteLdKBNAX0JuE8iPvGiWS0Z"
    
    # Simple request
    response = requests.post(
        "http://localhost:8000/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say hello in 5 words!"}],
            "max_tokens": 20
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success!")
        print(f"Response: {result['response']}")
        print(f"Cost: ${result['cost']:.6f}")
        print(f"Remaining Credits: ${result['remaining_credits']:.2f}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("🚀 Minimal UniLLM Client Test")
    print("=" * 40)
    print("This example uses only:")
    print("- requests (usually pre-installed)")
    print("- json (built into Python)")
    print("=" * 40)
    
    test_unillm_minimal() 