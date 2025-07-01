#!/usr/bin/env python3
"""
Test which Anthropic models are available to your API key.
"""
import os
import requests

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") or "your-anthropic-key-here"
if not ANTHROPIC_API_KEY or "sk-" not in ANTHROPIC_API_KEY:
    print("❌ Please set your ANTHROPIC_API_KEY environment variable.")
    exit(1)

url = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

models = [
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
]

for model in models:
    data = {
        "model": model,
        "max_tokens": 32,
        "messages": [
            {"role": "user", "content": f"Hello, are you {model}?"}
        ]
    }
    print(f"\nTesting model: {model}")
    try:
        response = requests.post(url, headers=headers, json=data)
        print("Status:", response.status_code)
        if response.status_code == 200:
            print(f"✅ Model '{model}' is available!")
            print("Response:", response.text)
        else:
            print(f"❌ Model '{model}' not available. Response:", response.text)
    except Exception as e:
        print(f"❌ Exception for model '{model}':", e) 