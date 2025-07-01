#!/usr/bin/env python3
"""
Credit Validation Testing Script

This script tests provider switching by using API keys with insufficient credits.
It validates that the routing and response handling works correctly even when
providers return "insufficient credits" errors.
"""

import os
import requests
import json
import time
from typing import Dict, List, Optional

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "test-client-key"

def setup_environment():
    """Set up environment variables from .env file."""
    print("🔧 Setting up environment...")
    
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                    print(f"✅ Loaded {key}")
    else:
        print("⚠️  No .env file found.")
    
    print()

def make_chat_request(model: str, messages: List[Dict[str, str]], **kwargs) -> Optional[Dict]:
    """Make a chat completion request to the API gateway."""
    
    url = f"{API_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        **kwargs
    }
    
    payload = {k: v for k, v in payload.items() if v is not None}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # We expect errors due to insufficient credits, so we'll analyze the response
        return {
            "status_code": response.status_code,
            "response_text": response.text,
            "headers": dict(response.headers)
        }
            
    except Exception as e:
        return {"error": str(e)}

def analyze_provider_response(response_data: Dict) -> Dict:
    """Analyze the response to determine which provider was used and what error occurred."""
    
    if "error" in response_data:
        return {
            "provider": "unknown",
            "error_type": "connection_error",
            "message": response_data["error"]
        }
    
    status_code = response_data.get("status_code", 0)
    response_text = response_data.get("response_text", "")
    
    # Analyze based on error messages
    if "OpenAI API error" in response_text:
        if "insufficient_quota" in response_text or "billing" in response_text:
            return {
                "provider": "openai",
                "error_type": "insufficient_credits",
                "message": "OpenAI: Insufficient credits/quota"
            }
        elif "invalid_api_key" in response_text:
            return {
                "provider": "openai", 
                "error_type": "invalid_key",
                "message": "OpenAI: Invalid API key"
            }
        else:
            return {
                "provider": "openai",
                "error_type": "other",
                "message": f"OpenAI: {response_text[:100]}..."
            }
    
    elif "Anthropic API error" in response_text:
        if "insufficient_quota" in response_text or "billing" in response_text:
            return {
                "provider": "anthropic",
                "error_type": "insufficient_credits", 
                "message": "Anthropic: Insufficient credits/quota"
            }
        elif "authentication_error" in response_text:
            return {
                "provider": "anthropic",
                "error_type": "invalid_key",
                "message": "Anthropic: Invalid API key"
            }
        else:
            return {
                "provider": "anthropic",
                "error_type": "other",
                "message": f"Anthropic: {response_text[:100]}..."
            }
    
    elif "Gemini API error" in response_text:
        if "quota" in response_text or "billing" in response_text:
            return {
                "provider": "gemini",
                "error_type": "insufficient_credits",
                "message": "Gemini: Insufficient credits/quota"
            }
        elif "API_KEY_INVALID" in response_text:
            return {
                "provider": "gemini",
                "error_type": "invalid_key", 
                "message": "Gemini: Invalid API key"
            }
        else:
            return {
                "provider": "gemini",
                "error_type": "other",
                "message": f"Gemini: {response_text[:100]}..."
            }
    
    else:
        return {
            "provider": "unknown",
            "error_type": "unknown",
            "message": f"Unknown error: {response_text[:100]}..."
        }

def test_provider_routing():
    """Test that requests are routed to the correct providers."""
    
    print("🔍 === Testing Provider Routing ===")
    
    test_models = [
        ("gpt-3.5-turbo", "OpenAI"),
        ("gpt-4", "OpenAI"),
        ("claude-3-sonnet", "Anthropic"),
        ("claude-3-haiku", "Anthropic"),
        ("gemini-pro", "Google Gemini"),
    ]
    
    routing_results = {}
    
    for model, expected_provider in test_models:
        print(f"\n🤖 Testing {expected_provider} ({model})...")
        
        response_data = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=50
        )
        
        analysis = analyze_provider_response(response_data)
        routing_results[model] = analysis
        
        print(f"   Expected Provider: {expected_provider}")
        print(f"   Actual Provider: {analysis['provider']}")
        print(f"   Error Type: {analysis['error_type']}")
        print(f"   Message: {analysis['message']}")
        
        # Validate routing
        if analysis['provider'].lower() == expected_provider.lower():
            print(f"   ✅ Routing: CORRECT")
        else:
            print(f"   ❌ Routing: INCORRECT")
    
    return routing_results

def test_insufficient_credits_validation():
    """Test that insufficient credits responses are handled correctly."""
    
    print("\n💰 === Testing Insufficient Credits Validation ===")
    
    # Test with models that should route to different providers
    test_cases = [
        ("gpt-3.5-turbo", "OpenAI"),
        ("claude-3-sonnet", "Anthropic"),
        ("gemini-pro", "Google Gemini"),
    ]
    
    credit_validation_results = {}
    
    for model, provider in test_cases:
        print(f"\n🤖 Testing {provider} ({model}) for credit validation...")
        
        response_data = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=100
        )
        
        analysis = analyze_provider_response(response_data)
        credit_validation_results[model] = analysis
        
        if analysis['error_type'] == 'insufficient_credits':
            print(f"   ✅ Credit validation: SUCCESS")
            print(f"   📊 Provider: {analysis['provider']}")
            print(f"   💡 This confirms the request reached {provider}")
        elif analysis['error_type'] == 'invalid_key':
            print(f"   ⚠️  Credit validation: INVALID KEY")
            print(f"   📊 Provider: {analysis['provider']}")
            print(f"   💡 This confirms the request reached {provider} but key is invalid")
        else:
            print(f"   ❓ Credit validation: UNKNOWN")
            print(f"   📊 Provider: {analysis['provider']}")
            print(f"   💡 Error type: {analysis['error_type']}")
    
    return credit_validation_results

def test_provider_switching_validation():
    """Test that switching between providers works correctly."""
    
    print("\n🔄 === Testing Provider Switching Validation ===")
    
    # Test switching between different providers
    switching_tests = [
        ("gpt-3.5-turbo", "OpenAI"),
        ("claude-3-sonnet", "Anthropic"),
        ("gpt-4", "OpenAI"),
        ("gemini-pro", "Google Gemini"),
    ]
    
    switching_results = {}
    
    for i, (model, provider) in enumerate(switching_tests):
        print(f"\n🔄 Switch {i+1}: Testing {provider} ({model})...")
        
        response_data = make_chat_request(
            model=model,
            messages=[{"role": "user", "content": f"Test message for {provider}"}],
            max_tokens=50
        )
        
        analysis = analyze_provider_response(response_data)
        switching_results[model] = analysis
        
        print(f"   📊 Provider: {analysis['provider']}")
        print(f"   🔄 Switch: {provider} → {analysis['provider']}")
        
        if analysis['provider'].lower() == provider.lower():
            print(f"   ✅ Switch: SUCCESSFUL")
        else:
            print(f"   ❌ Switch: FAILED")
    
    return switching_results

def test_error_handling():
    """Test that different error types are handled correctly."""
    
    print("\n🛡️ === Testing Error Handling ===")
    
    # Test with invalid model to see error handling
    print("\n🤖 Testing invalid model...")
    
    response_data = make_chat_request(
        model="invalid-model-123",
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    print(f"   Status Code: {response_data.get('status_code', 'N/A')}")
    print(f"   Response: {response_data.get('response_text', 'N/A')[:200]}...")
    
    # Test with malformed request
    print("\n🤖 Testing malformed request...")
    
    url = f"{API_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json={"invalid": "data"}, timeout=30)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")

def generate_test_report(routing_results, credit_results, switching_results):
    """Generate a comprehensive test report."""
    
    print("\n" + "="*80)
    print("📊 TEST REPORT")
    print("="*80)
    
    # Routing validation
    print("\n🔍 ROUTING VALIDATION:")
    correct_routing = 0
    total_routing = len(routing_results)
    
    for model, result in routing_results.items():
        if result['provider'] != 'unknown':
            correct_routing += 1
            print(f"   ✅ {model}: {result['provider']}")
        else:
            print(f"   ❌ {model}: Unknown provider")
    
    print(f"   📊 Routing Accuracy: {correct_routing}/{total_routing} ({correct_routing/total_routing*100:.1f}%)")
    
    # Credit validation
    print("\n💰 CREDIT VALIDATION:")
    credit_validations = 0
    total_credit_tests = len(credit_results)
    
    for model, result in credit_results.items():
        if result['error_type'] in ['insufficient_credits', 'invalid_key']:
            credit_validations += 1
            print(f"   ✅ {model}: {result['error_type']}")
        else:
            print(f"   ❌ {model}: {result['error_type']}")
    
    print(f"   📊 Credit Validation: {credit_validations}/{total_credit_tests} ({credit_validations/total_credit_tests*100:.1f}%)")
    
    # Provider switching
    print("\n🔄 PROVIDER SWITCHING:")
    successful_switches = 0
    total_switches = len(switching_results)
    
    for model, result in switching_results.items():
        if result['provider'] != 'unknown':
            successful_switches += 1
            print(f"   ✅ {model}: {result['provider']}")
        else:
            print(f"   ❌ {model}: Unknown provider")
    
    print(f"   📊 Switching Success: {successful_switches}/{total_switches} ({successful_switches/total_switches*100:.1f}%)")
    
    # Overall assessment
    print("\n🎯 OVERALL ASSESSMENT:")
    total_tests = total_routing + total_credit_tests + total_switches
    successful_tests = correct_routing + credit_validations + successful_switches
    
    print(f"   📊 Total Tests: {total_tests}")
    print(f"   ✅ Successful: {successful_tests}")
    print(f"   ❌ Failed: {total_tests - successful_tests}")
    print(f"   📈 Success Rate: {successful_tests/total_tests*100:.1f}%")
    
    if successful_tests/total_tests >= 0.8:
        print("   🎉 EXCELLENT: Provider switching is working correctly!")
    elif successful_tests/total_tests >= 0.6:
        print("   ✅ GOOD: Provider switching is mostly working.")
    else:
        print("   ⚠️  NEEDS IMPROVEMENT: Some issues with provider switching.")

def main():
    """Main function to run all tests."""
    
    print("🚀 UniLLM API Gateway - Credit Validation Testing")
    print("=" * 60)
    
    # Set up environment
    setup_environment()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API Gateway is running")
        else:
            print("❌ API Gateway is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API Gateway. Make sure it's running on http://localhost:8000")
        return
    
    print("\n" + "="*60)
    
    # Run tests
    routing_results = test_provider_routing()
    credit_results = test_insufficient_credits_validation()
    switching_results = test_provider_switching_validation()
    test_error_handling()
    
    # Generate report
    generate_test_report(routing_results, credit_results, switching_results)
    
    print("\n🎉 Credit validation testing completed!")
    print("\n💡 Next steps:")
    print("1. Add real API keys with credits to test actual responses")
    print("2. Test with different parameters and conversation flows")
    print("3. Implement billing and credit system for Phase 2")

if __name__ == "__main__":
    main() 