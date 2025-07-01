# UniLLM API Gateway - Quick Start Guide

## 🚀 What We've Built

You now have a fully functional API gateway that allows you to:

- **Switch between LLM providers seamlessly** using a single API
- **Use one API key** to access all providers (OpenAI, Anthropic, Gemini, Mistral, Cohere)
- **Continue conversations** across different providers
- **Compare responses** from different models

## 📁 Project Structure

```
api_gateway/
├── main.py                    # FastAPI server with provider adapters
├── requirements.txt           # Python dependencies
├── unillm_client.py          # Python client library
├── test_provider_switching.py # Test script
├── demo_with_real_keys.py    # Demo with real API keys
├── README.md                 # Detailed documentation
├── env_example.txt           # Environment variables template
└── .env                      # Your API keys (create this)
```

## ⚡ Quick Start

### 1. Start the API Gateway

```bash
cd api_gateway
python main.py
```

The server will start on `http://localhost:8000`

### 2. Test the API

```bash
# Health check
curl http://localhost:8000/health

# List available models
curl http://localhost:8000/models

# Test a chat request (will fail without real API keys)
curl -X POST "http://localhost:8000/chat/completions" \
  -H "Authorization: Bearer test-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### 3. Use the Python Client

```python
from unillm_client import create_client, create_session

# Create client
client = create_client()

# Create chat session
session = create_session(client)

# Chat with OpenAI
response1 = session.chat("Hello!", model="gpt-4")
print(f"OpenAI: {response1['content']}")

# Switch to Anthropic
response2 = session.switch_provider("claude-3-sonnet")
print(f"Anthropic: {response2['content']}")

# Continue with Gemini
response3 = session.chat("Tell me more", model="gemini-pro")
print(f"Gemini: {response3['content']}")
```

## 🔑 Setting Up Real API Keys

1. **Copy the environment template:**
   ```bash
   cp env_example.txt .env
   ```

2. **Edit `.env` with your API keys:**
   ```bash
   OPENAI_API_KEY=sk-your-openai-key
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
   GEMINI_API_KEY=your-gemini-key
   MISTRAL_API_KEY=your-mistral-key
   COHERE_API_KEY=your-cohere-key
   ```

3. **Restart the API gateway:**
   ```bash
   python main.py
   ```

## 🎯 Provider Switching Examples

### Basic Switching

```python
# Ask the same question to different providers
question = "What is the capital of France?"

# OpenAI
response1 = client.chat("gpt-4", [{"role": "user", "content": question}])

# Anthropic  
response2 = client.chat("claude-3-sonnet", [{"role": "user", "content": question}])

# Gemini
response3 = client.chat("gemini-pro", [{"role": "user", "content": question}])

print(f"OpenAI: {response1['content']}")
print(f"Anthropic: {response2['content']}")
print(f"Gemini: {response3['content']}")
```

### Conversation Switching

```python
# Start conversation with OpenAI
session = create_session(client)
response1 = session.chat("I want to visit Paris", model="gpt-4")

# Continue with Anthropic
response2 = session.chat("What about the best time to visit?", model="claude-3-sonnet")

# Finish with Gemini
response3 = session.chat("What about transportation?", model="gemini-pro")
```

## 📊 Available Models

| Provider | Models |
|----------|--------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-3.5-turbo, gpt-3.5-turbo-16k |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku |
| Google | gemini-pro, gemini-pro-vision, gemini-1.5-pro |
| Mistral | mistral-large, mistral-medium, mistral-small |
| Cohere | command, command-light |

## 🔧 API Endpoints

- `GET /health` - Health check
- `GET /models` - List available models
- `POST /chat/completions` - Send chat request

## 🛠️ Development

### Adding New Providers

1. Create adapter class in `main.py`
2. Add to `get_adapter()` function
3. Add models to `MODEL_PROVIDER_MAP`
4. Add API key to `PROVIDER_KEYS`

### Running in Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🎉 What You Can Do Now

1. **Switch between providers** by changing the model name
2. **Compare responses** from different models
3. **Continue conversations** across providers
4. **Use a unified interface** for all LLM providers
5. **Scale easily** by adding more providers

## 🚀 Next Steps

- Add real API keys to test with actual providers
- Implement streaming responses
- Add rate limiting and caching
- Build a web UI
- Add authentication and user management
- Deploy to production

## 📚 Documentation

- Full API documentation: `http://localhost:8000/docs`
- Interactive API explorer: `http://localhost:8000/redoc`

---

**🎯 Goal Achieved:** You can now get responses from OpenAI and switch to Gemini (or any other provider) seamlessly using a single API! 