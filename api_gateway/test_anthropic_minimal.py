#!/usr/bin/env python3
"""
Minimal test for Anthropic via UniLLM API Gateway.
"""
import os
import sys

# Add src to path if running from api_gateway
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unillm import UniLLM, chat, UniLLMError

API_KEY = os.getenv("UNILLM_API_KEY")
MODEL = "claude-3-sonnet-20240229"  # Replace with your Anthropic model if needed

if not API_KEY:
    print("❌ UNILLM_API_KEY environment variable not set.")
    sys.exit(1)

client = UniLLM(api_key=API_KEY)

try:
    print(f"\n🧪 Testing Anthropic model: {MODEL}")
    messages = [
        {"role": "user", "content": "Hello Anthropic! What is 2+2?"}
    ]
    response = client.chat(model=MODEL, messages=messages)
    print(f"✅ Success! Response: {response.content}")
    print(f"Model: {response.model}")
    print(f"Usage: {response.usage}")
except UniLLMError as e:
    print(f"❌ UniLLMError: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 