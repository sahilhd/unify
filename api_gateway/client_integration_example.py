#!/usr/bin/env python3
"""
UniLLM Client Integration Example
This shows how a real client would use UniLLM in their own Python project.
"""

import requests
import json
import time
from typing import Dict, List, Optional

class UniLLMClient:
    """
    UniLLM Client for easy integration into any Python project
    """
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        """
        Initialize the UniLLM client
        
        Args:
            api_key: Your UniLLM API key (starts with 'unillm_')
            base_url: UniLLM server URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict:
        """
        Send a chat completion request
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (e.g., 'gpt-3.5-turbo', 'claude-3-sonnet')
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 2.0)
        
        Returns:
            Dictionary with response, cost, and remaining credits
        """
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"API Error: {error_data.get('detail', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
    
    def get_usage_stats(self) -> Dict:
        """Get usage statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/billing/usage",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to get usage stats"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {e}"}
    
    def purchase_credits(self, amount: float) -> Dict:
        """Purchase credits"""
        try:
            response = requests.post(
                f"{self.base_url}/billing/purchase-credits",
                headers=self.headers,
                json={"amount": amount},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"Purchase failed: {error_data.get('detail', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")


def main():
    """
    Example usage of UniLLM in a real project
    """
    
    # Step 1: Initialize the client with your API key
    # Replace this with your actual API key from UniLLM
    API_KEY = "unillm_A4hEQGsyBteLdKBNAX0JuE8iPvGiWS0Z"  # Replace with your key
    
    client = UniLLMClient(API_KEY)
    
    print("🤖 UniLLM Client Integration Example")
    print("=" * 50)
    
    # Step 2: Test different models
    models_to_test = [
        ("gpt-3.5-turbo", "OpenAI"),
        ("claude-3-sonnet", "Anthropic")
    ]
    
    for model, provider in models_to_test:
        print(f"\n🧪 Testing {provider} ({model})...")
        
        try:
            # Create a conversation
            messages = [
                {"role": "user", "content": f"Hello! I'm testing {provider}. Can you give me a brief introduction?"}
            ]
            
            # Send the request
            result = client.chat_completion(
                messages=messages,
                model=model,
                max_tokens=150,
                temperature=0.7
            )
            
            print(f"✅ {provider} Response:")
            print(f"   Response: {result['response']}")
            print(f"   Cost: ${result['cost']:.6f}")
            print(f"   Remaining Credits: ${result['remaining_credits']:.2f}")
            
        except Exception as e:
            print(f"❌ {provider} failed: {e}")
    
    # Step 3: Show usage statistics
    print(f"\n📊 Usage Statistics:")
    usage = client.get_usage_stats()
    if "error" not in usage:
        print(f"   Total Requests: {usage.get('total_requests', 0)}")
        print(f"   Total Cost: ${usage.get('total_cost', 0):.4f}")
        print(f"   Requests Today: {usage.get('requests_today', 0)}")
    else:
        print(f"   Error: {usage['error']}")
    
    # Step 4: Example of a more complex conversation
    print(f"\n💬 Complex Conversation Example:")
    
    conversation = [
        {"role": "user", "content": "I'm building a Python web application. Can you help me with some coding questions?"},
        {"role": "assistant", "content": "Of course! I'd be happy to help you with your Python web application. What specific questions do you have about coding?"},
        {"role": "user", "content": "What's the best way to handle environment variables in a Flask app?"}
    ]
    
    try:
        result = client.chat_completion(
            messages=conversation,
            model="gpt-3.5-turbo",
            max_tokens=300,
            temperature=0.5
        )
        
        print(f"✅ Response: {result['response']}")
        print(f"   Cost: ${result['cost']:.6f}")
        
    except Exception as e:
        print(f"❌ Conversation failed: {e}")


def advanced_example():
    """
    Advanced example showing more sophisticated usage
    """
    
    API_KEY = "unillm_A4hEQGsyBteLdKBNAX0JuE8iPvGiWS0Z"  # Replace with your key
    client = UniLLMClient(API_KEY)
    
    print("\n🚀 Advanced Usage Example")
    print("=" * 50)
    
    # Example: Code review assistant
    code_to_review = '''
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    '''
    
    review_prompt = f"""
    Please review this Python function and suggest improvements:
    
    {code_to_review}
    
    Focus on:
    1. Performance issues
    2. Best practices
    3. Alternative approaches
    """
    
    try:
        result = client.chat_completion(
            messages=[{"role": "user", "content": review_prompt}],
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.3
        )
        
        print("🔍 Code Review Result:")
        print(result['response'])
        print(f"\n💰 Cost: ${result['cost']:.6f}")
        
    except Exception as e:
        print(f"❌ Code review failed: {e}")


if __name__ == "__main__":
    # Run the basic example
    main()
    
    # Run the advanced example
    advanced_example()
    
    print("\n🎉 Integration complete!")
    print("\n💡 Tips for production use:")
    print("1. Store your API key in environment variables")
    print("2. Add error handling and retries")
    print("3. Monitor usage and costs")
    print("4. Consider rate limiting in your application") 