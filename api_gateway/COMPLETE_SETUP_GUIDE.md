# UniLLM Complete Setup Guide

## Overview

This guide shows the complete flow from deploying UniLLM to using it as an end user.

## Part 1: Service Provider Setup (One-time)

### Step 1: Deploy UniLLM Server

```bash
# 1. Clone the repository
git clone <your-unillm-repo>
cd api_gateway

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements_phase2.txt

# 4. Set up environment variables
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
export GOOGLE_API_KEY="your-google-key"
export JWT_SECRET="your-secret-key"

# 5. Start the server
python main_phase2.py
```

### Step 2: Deploy to Cloud (Optional)

```bash
# Example: Deploy to Heroku
heroku create your-unillm-app
git push heroku main

# Your API will be available at:
# https://your-unillm-app.herokuapp.com
```

### Step 3: Launch Dashboard

```bash
# In a new terminal
python launch_dashboard.py

# Dashboard available at: http://localhost:8501
```

## Part 2: End User Setup (One-time per user)

### Step 1: Register Account

1. Go to your dashboard: `http://localhost:8501` (or your cloud URL)
2. Click "Register"
3. Enter email and password
4. Copy your API key (starts with `unillm_`)

### Step 2: Add Credits

1. In the dashboard, go to "Billing"
2. Click "Purchase Credits"
3. Add credits to your account

## Part 3: Using UniLLM (Daily usage)

### Method 1: Using the Client Library

```bash
# Download the client library
curl -O https://your-server.com/unillm_client_library.py
```

```python
# your_script.py
from unillm_client_library import UniLLMClient

# Initialize with your API key
client = UniLLMClient("unillm_your_key_here")

# Use exactly like OpenAI
response = client.ChatCompletion().create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's the capital of France?"}
    ],
    max_tokens=100
)

print(response.choices[0].message.content)
print(f"Provider: {response.provider}")
print(f"Cost: ${response.cost:.6f}")
```

### Method 2: Using Raw HTTP Requests

```python
import requests

# Simple chat request
response = requests.post(
    "http://localhost:8000/chat/completions",
    headers={
        "Authorization": "Bearer unillm_your_key_here",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": "Hello!"}
        ],
        "max_tokens": 50
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### Method 3: Using curl

```bash
curl -X POST http://localhost:8000/chat/completions \
  -H "Authorization: Bearer unillm_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 50
  }'
```

## Part 4: Model Switching Examples

### Switch Between Providers

```python
from unillm_client_library import UniLLMClient

client = UniLLMClient("unillm_your_key_here")

# OpenAI GPT-4o
response1 = client.ChatCompletion().create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain AI"}]
)

# Anthropic Claude-3-sonnet
response2 = client.ChatCompletion().create(
    model="claude-3-sonnet",
    messages=[{"role": "user", "content": "Explain AI"}]
)

# Google Gemini Pro
response3 = client.ChatCompletion().create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Explain AI"}]
)

print(f"OpenAI: {response1.choices[0].message.content}")
print(f"Anthropic: {response2.choices[0].message.content}")
print(f"Google: {response3.choices[0].message.content}")
```

## Part 5: Advanced Usage

### Get Usage Statistics

```python
# Get your usage stats
usage = client.get_usage_stats()
print(f"Total requests: {usage['total_requests']}")
print(f"Total cost: ${usage['total_cost']:.6f}")
```

### Purchase More Credits

```python
# Purchase additional credits
result = client.purchase_credits(50.0)
print(f"Credits added: {result['credits_added']}")
print(f"New balance: {result['new_balance']}")
```

### Multi-turn Conversations

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's 2+2?"},
    {"role": "assistant", "content": "2+2 equals 4."},
    {"role": "user", "content": "What about 3+3?"}
]

response = client.ChatCompletion().create(
    model="claude-3-sonnet",
    messages=messages,
    max_tokens=100
)

print(response.choices[0].message.content)
```

## Part 6: Migration from OpenAI

### Before (OpenAI)
```python
import openai
openai.api_key = "sk-..."

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### After (UniLLM)
```python
from unillm_client_library import UniLLMClient

client = UniLLMClient("unillm_your_key_here")

response = client.ChatCompletion().create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**That's it!** The API is identical.

## Part 7: Troubleshooting

### Common Issues

1. **"Invalid API key"**
   - Make sure you copied the full API key from the dashboard
   - API keys start with `unillm_`

2. **"Insufficient credits"**
   - Purchase more credits in the dashboard
   - Check your current balance

3. **"Model not available"**
   - Check the available models list
   - Make sure the model name is correct

4. **Connection errors**
   - Verify the server is running
   - Check the correct URL/port

### Testing Your Setup

```bash
# Test the server health
curl http://localhost:8000/health

# Test with a simple request
python test_client_library.py
```

## Summary

1. **Deploy** UniLLM server (one-time)
2. **Register** user account (one-time per user)
3. **Get API key** from dashboard
4. **Use** exactly like OpenAI library
5. **Switch models** by changing model name
6. **Monitor usage** through dashboard

That's the complete flow! Users get a seamless experience with the power to switch between any LLM provider. 