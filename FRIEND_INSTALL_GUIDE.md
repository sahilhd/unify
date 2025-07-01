# 🚀 UniLLM - Friend Installation Guide

## Quick Install from PyPI

Your friend can install UniLLM directly from PyPI:

```bash
# Install the UniLLM client library
pip install unillm

# Or install with extra features
pip install unillm[all]
```

## Usage Examples

### 1. Basic API Usage
```python
import requests

# Your deployed server URL (you'll provide this)
BASE_URL = "https://your-unillm-server.railway.app"
API_KEY = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0"

# Test OpenAI
response = requests.post(
    f"{BASE_URL}/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(response.json())
```

### 2. Using the UniLLM Client Library
```python
from unillm import UniLLMClient

# Connect to your server
client = UniLLMClient(
    api_key="unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0",
    base_url="https://your-unillm-server.railway.app"
)

# Test OpenAI
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello from OpenAI!"}]
)
print(response.response)

# Test Anthropic
response = client.chat.completions.create(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Hello from Anthropic!"}]
)
print(response.response)
```

### 3. Available Models
```python
# List all available models
models = client.models.list()
for model in models.data:
    print(f"{model.id} ({model.provider})")
```

## Dashboard Access

If you deploy the frontend:
- **URL**: https://your-unillm-server.railway.app
- **Login**: sah@gmail.com / 123

## What Your Friend Gets

✅ **Unified API** for OpenAI + Anthropic  
✅ **Python Client Library**  
✅ **Usage Tracking**  
✅ **Cost Monitoring**  
✅ **Model Aliases** (gpt-4, claude-3-sonnet, etc.)  
✅ **Modern Dashboard** (if deployed)  

## Testing Checklist

Your friend should test:
- [ ] OpenAI GPT-3.5-turbo
- [ ] OpenAI GPT-4  
- [ ] Anthropic Claude-3-Opus
- [ ] Anthropic Claude-3-Sonnet
- [ ] Anthropic Claude-3-Haiku
- [ ] Model listing
- [ ] Usage tracking
- [ ] Dashboard login (if available)

## Support

If they have issues:
1. Check the API key is correct
2. Verify the server URL is accessible
3. Check their internet connection
4. Contact you for the latest server URL 