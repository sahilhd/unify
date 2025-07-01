# UniLLM API Gateway

A FastAPI server that provides a unified interface for multiple LLM providers (OpenAI, Anthropic, Google Gemini, etc.).

## Features

- 🔑 **Single API Key**: Use one key to access all providers
- 🎯 **Unified Interface**: Same API for all providers
- 🔄 **Easy Provider Switching**: Switch between providers seamlessly
- 📊 **Consistent Responses**: Standardized response format
- 🛡️ **Error Handling**: Comprehensive error handling
- 📚 **Auto-generated Docs**: Interactive API documentation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file and add your API keys:

```bash
cp env_example.txt .env
```

Edit `.env` and add your actual API keys:

```bash
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GEMINI_API_KEY=your-gemini-key
```

### 3. Start the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### 4. Test the API

Visit `http://localhost:8000/docs` for interactive API documentation.

## API Endpoints

### Chat Completions

**POST** `/chat/completions`

Send a chat completion request to any supported model.

```bash
curl -X POST "http://localhost:8000/chat/completions" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

### List Models

**GET** `/models`

Get a list of all available models and their providers.

```bash
curl "http://localhost:8000/models"
```

### Health Check

**GET** `/health`

Check if the API gateway is running.

```bash
curl "http://localhost:8000/health"
```

## Supported Models

| Provider | Models |
|----------|--------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-3.5-turbo, gpt-3.5-turbo-16k |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku |
| Google | gemini-pro, gemini-pro-vision, gemini-1.5-pro |
| Mistral | mistral-large, mistral-medium, mistral-small |
| Cohere | command, command-light |

## Usage Examples

### Python Client

```python
import requests

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "your-api-key"

# Test OpenAI
response = requests.post(
    f"{API_BASE_URL}/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(f"OpenAI: {response.json()['content']}")

# Switch to Anthropic
response = requests.post(
    f"{API_BASE_URL}/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "claude-3-sonnet",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(f"Anthropic: {response.json()['content']}")

# Switch to Gemini
response = requests.post(
    f"{API_BASE_URL}/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gemini-pro",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(f"Gemini: {response.json()['content']}")
```

### Using the UniLLM Python Library

```python
from unillm import ChatLLM

# Configure the library to use your API gateway
ChatLLM.api_key = "your-api-key"
ChatLLM.base_url = "http://localhost:8000"

# Switch between providers seamlessly
response1 = ChatLLM.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(f"OpenAI: {response1.content}")

response2 = ChatLLM.chat(
    model="claude-3-sonnet",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(f"Anthropic: {response2.content}")

response3 = ChatLLM.chat(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(f"Gemini: {response3.content}")
```

## Testing

Run the test script to see provider switching in action:

```bash
python test_provider_switching.py
```

This will demonstrate:
- Switching between different providers
- Continuing conversations across providers
- Comparing responses from different models

## Response Format

All responses follow this format:

```json
{
  "content": "The generated text",
  "model": "gpt-4",
  "provider": "openai",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  },
  "finish_reason": "stop",
  "created_at": "2024-01-01T12:00:00"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid model or request format
- `401 Unauthorized`: Invalid API key
- `500 Internal Server Error`: Provider API error or configuration issue

## Development

### Adding New Providers

1. Create a new adapter class in `main.py`
2. Add the provider to the `get_adapter()` function
3. Add models to `MODEL_PROVIDER_MAP`
4. Add API key to `PROVIDER_KEYS`

### Running in Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production deployment:

1. Use a proper WSGI server (Gunicorn)
2. Set up proper authentication
3. Add rate limiting
4. Use environment variables for configuration
5. Set up monitoring and logging

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## License

MIT License 