# 🔑 Your UniLLM API Key

## Your API Key
```
unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0
```

## 📧 Account Details
- **Email**: sah@gmail.com
- **Credits**: $10.0
- **Status**: Active

## 🚀 How to Use Your API Key

### 1. Test Your API Key
```bash
# Run the standalone test
python test_api_key_standalone.py

# Or use the curl test
curl -X POST http://localhost:8000/chat/completions \
  -H "Authorization: Bearer unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### 2. Python Example
```python
import requests

api_key = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0"
url = "http://localhost:8000/chat/completions"

response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)

print(response.json())
```

### 3. JavaScript Example
```javascript
const apiKey = "unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0";
const url = "http://localhost:8000/chat/completions";

fetch(url, {
    method: "POST",
    headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [{role: "user", content: "Hello!"}]
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📊 Available Models

### OpenAI
- `gpt-3.5-turbo` ✅ (Working)
- `gpt-4`
- `gpt-4-turbo`

### Anthropic
- `claude-3-sonnet` (Needs credits)
- `claude-3-haiku`
- `claude-3-opus`

### Google
- `gemini-pro` (Needs API key)
- `gemini-flash`

### Mistral
- `mistral-7b` (Needs API key)
- `mixtral-8x7b`

### Cohere
- `command` (Needs API key)
- `command-r`

## 💰 Billing

- **Current Balance**: $10.0
- **Cost per request**: ~$0.00002 (varies by model)
- **Purchase more credits**: Use the dashboard or API

## 🔧 Troubleshooting

### If you get "Invalid API key":
1. Make sure you copied the full key
2. Check that the server is running on localhost:8000
3. Verify your account has credits

### If you get "Insufficient credits":
1. Purchase more credits through the dashboard
2. Or use the API: `POST /billing/purchase-credits`

### If the server is not responding:
1. Start the server: `python main_phase2.py`
2. Check the logs: `tail -f server_phase2.log`

## 🌐 Dashboard Access

Visit the web dashboard at: http://localhost:8501
- Login with: sah@gmail.com
- View your full API key
- Monitor usage and costs
- Purchase credits

## 📝 Quick Commands

```bash
# Get your API key
python get_api_key.py

# Test your API key
python test_api_key_standalone.py

# Start the server
python main_phase2.py

# Launch dashboard
python launch_dashboard.py
```

---
**Keep this API key secure!** It provides access to your account and credits. 