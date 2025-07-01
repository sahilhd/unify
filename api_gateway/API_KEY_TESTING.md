# UniLLM API Key Testing Guide

This guide shows you how to test your UniLLM API key in a fresh project or environment.

## 🚀 Quick Test Options

### Option 1: Python Script (Recommended)
```bash
python test_api_key_standalone.py
```

### Option 2: Curl Script
```bash
./test_api_key_curl.sh
```

### Option 3: Manual Curl Commands
```bash
# Replace YOUR_API_KEY with your actual UniLLM API key
API_KEY="unillm_YOUR_ACTUAL_KEY_HERE"

# Test health
curl http://localhost:8000/health

# Test chat completion
curl -X POST http://localhost:8000/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

## 📋 Prerequisites

1. **UniLLM Server Running**: Make sure your UniLLM server is running on `localhost:8000`
2. **Valid API Key**: You need a UniLLM API key (starts with `unillm_`)
3. **Python Dependencies**: For the Python script, you need `requests`:
   ```bash
   pip install requests
   ```

## 🔑 Getting Your API Key

1. **Register a user** (if you haven't already):
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123"}'
   ```

2. **Login to get your API key**:
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123"}'
   ```

3. **Copy the API key** from the response (starts with `unillm_`)

## 🧪 What the Tests Do

### 1. Health Check
- Verifies the server is running and healthy
- Shows server version and features

### 2. Chat Completion
- Sends a test message to GPT-3.5-turbo
- Verifies authentication and billing work
- Shows response, cost, and remaining credits

### 3. Usage Stats
- Retrieves your usage statistics
- Shows total requests, costs, and daily usage

## 📊 Expected Output

If everything works, you should see:
```
🚀 UniLLM API Key Test
====================================
🔑 Testing UniLLM API Key: unillm_ABC123...
🌐 Server URL: http://localhost:8000

1️⃣ Testing server health...
✅ Server is healthy!
   Version: 2.0.0
   Features: authentication, billing, rate_limiting

2️⃣ Testing chat completion...
✅ Chat completion successful!
   Response: Hello from UniLLM!
   Provider: openai
   Cost: 2.4e-05
   Remaining Credits: 9.999976

3️⃣ Testing usage stats...
✅ Usage stats retrieved!
   Total Requests: 1
   Total Cost: 2.4e-05
   Requests Today: 1

====================================
🎉 API Key test completed!
✅ Your API key is working correctly!
```

## 🔧 Troubleshooting

### Server Not Running
```
❌ Cannot connect to server: Connection refused
```
**Solution**: Start your UniLLM server:
```bash
python main_phase2.py
```

### Invalid API Key
```
❌ Chat completion failed: 401
   Error: Invalid authentication credentials
```
**Solution**: Check your API key format and make sure it starts with `unillm_`

### Insufficient Credits
```
❌ Chat completion failed: 402
   Error: Insufficient credits
```
**Solution**: Purchase more credits:
```bash
curl -X POST http://localhost:8000/billing/purchase-credits \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10.0}'
```

## 💡 Using Your API Key in Other Projects

Once your API key is working, you can use it in any project:

### Python Example
```python
import requests

api_key = "unillm_YOUR_ACTUAL_KEY_HERE"
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

### JavaScript Example
```javascript
const apiKey = "unillm_YOUR_ACTUAL_KEY_HERE";
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

## 🎯 Next Steps

After testing your API key:
1. **Integrate it** into your applications
2. **Add more providers** (Anthropic, Google, etc.)
3. **Set up billing** for production use
4. **Deploy the server** to a cloud provider 