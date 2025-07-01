#!/usr/bin/env python3
"""
Test switching between OpenAI and Anthropic via UniLLM API Gateway.
"""
import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from unillm import UniLLM, UniLLMError

# Use the correct UniLLM API key
API_KEY = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0"
BASE_URL = "http://localhost:8000"

client = UniLLM(api_key=API_KEY)

models_to_test = [
    ("OpenAI", "gpt-3.5-turbo"),
    ("OpenAI", "gpt-4"),
    ("Anthropic", "claude-3-opus-20240229"),
    ("Anthropic", "claude-3-haiku-20240307"),
]

for provider, model in models_to_test:
    print(f"\n🧪 Testing {provider} model: {model}")
    try:
        messages = [
            {"role": "user", "content": f"Hello, this is a test for {provider} model {model}."}
        ]
        response = client.chat(model=model, messages=messages)
        print(f"✅ {provider} {model} response: {response.content}")
    except Exception as e:
        print(f"❌ {provider} {model} error: {e}")

# Step 4: Test provider switching in same conversation
print("\n4️⃣ Testing provider switching...")
try:
    # First message with OpenAI
    headers = {"Authorization": f"Bearer {API_KEY}"}
    chat_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "What is 2+2? Answer briefly."}
        ],
        "max_tokens": 20
    }
    response1 = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=chat_data, timeout=60)
    
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"✅ OpenAI response: {result1.get('response', 'N/A')}")
        
        # Same question with Anthropic
        chat_data["model"] = "claude-3-opus-20240229"
        response2 = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=chat_data, timeout=60)
        
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✅ Anthropic response: {result2.get('response', 'N/A')}")
            print(f"   Different providers, same question!")
        else:
            print(f"❌ Anthropic switch failed: {response2.status_code} - {response2.text}")
    else:
        print(f"❌ OpenAI switch failed: {response1.status_code} - {response1.text}")
        
except Exception as e:
    print(f"❌ Provider switching error: {e}")

# Step 5: Check final usage stats
print("\n5️⃣ Final usage stats...")
try:
    response = requests.get(
        f"{BASE_URL}/billing/usage",
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=10
    )
    if response.status_code == 200:
        usage_data = response.json()
        print(f"✅ Usage stats:")
        print(f"   Total requests: {usage_data.get('total_requests', 0)}")
        print(f"   Total cost: {usage_data.get('total_cost', 0)}")
        print(f"   Requests today: {usage_data.get('requests_today', 0)}")
    else:
        print(f"❌ Usage stats failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Usage stats error: {e}")

print("\n🎉 Multi-provider testing completed!") 