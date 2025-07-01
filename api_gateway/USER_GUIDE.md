# UniLLM User Guide

## What is UniLLM?

UniLLM is a unified API gateway that allows you to use multiple LLM providers (OpenAI, Anthropic, Google, etc.) with a single API key. It's designed to be a **drop-in replacement** for the OpenAI Python library.

## Key Benefits

✅ **Single API Key**: Use one key for all providers  
✅ **OpenAI-Compatible**: Works exactly like the OpenAI library  
✅ **Easy Model Switching**: Change providers by just changing the model name  
✅ **Unified Billing**: Pay for all providers through one system  
✅ **Usage Tracking**: Monitor costs and usage across all providers  

## Quick Start

### 1. Get Your API Key

1. Register at your UniLLM dashboard: `http://your-server:8501`
2. Copy your API key (starts with `unillm_`)

### 2. Install the Client Library

```bash
# Option 1: Copy the client file
cp unillm_client_library.py your_project/

# Option 2: Install via pip (when published)
pip install unillm-client
```

### 3. Use Like OpenAI

```python
from unillm_client_library import UniLLMClient

# Initialize (just like OpenAI)
client = UniLLMClient("your_unillm_api_key_here")

# Use GPT-4o (OpenAI)
response = client.ChatCompletion().create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=100
)

print(response.choices[0].message.content)
```

### 4. Switch Models Seamlessly

```python
# Same code, different models!

# OpenAI GPT-4o
response = client.ChatCompletion().create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Anthropic Claude-3-sonnet
response = client.ChatCompletion().create(
    model="claude-3-sonnet",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Google Gemini Pro
response = client.ChatCompletion().create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Available Models

| Provider | Model Names | Description |
|----------|-------------|-------------|
| **OpenAI** | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo` | Latest GPT models |
| **Anthropic** | `claude-3-sonnet`, `claude-3-haiku`, `claude-3-opus` | Claude models |
| **Google** | `gemini-pro`, `gemini-pro-vision` | Gemini models |
| **Mistral** | `mistral-large`, `mistral-medium`, `mistral-small` | Mistral models |
| **Cohere** | `command`, `command-light` | Cohere models |

## Complete Examples

### Basic Usage

```python
from unillm_client_library import UniLLMClient

# Initialize
client = UniLLMClient("unillm_your_key_here")

# Simple chat
response = client.ChatCompletion().create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's 2+2?"}
    ],
    max_tokens=50
)

print(response.choices[0].message.content)
```

### Advanced Usage

```python
# Multi-turn conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What's the population?"}
]

response = client.ChatCompletion().create(
    model="claude-3-sonnet",
    messages=messages,
    max_tokens=200,
    temperature=0.7,
    top_p=0.9
)

print(f"Response: {response.choices[0].message.content}")
print(f"Provider: {response.provider}")
print(f"Cost: ${response.cost:.6f}")
print(f"Remaining credits: {response.remaining_credits}")
```

### Usage Statistics

```python
# Get usage stats
usage = client.get_usage_stats()
print(f"Total requests: {usage['total_requests']}")
print(f"Total tokens: {usage['total_tokens']}")
print(f"Total cost: ${usage['total_cost']:.6f}")
print(f"Requests today: {usage['requests_today']}")
```

### Purchase Credits

```python
# Purchase more credits
result = client.purchase_credits(50.0)
print(f"Credits added: {result['credits_added']}")
print(f"New balance: {result['new_balance']}")
```

## Migration from OpenAI

If you're currently using OpenAI, here's how to migrate:

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

**That's it!** The API is identical, just change the import and initialization.

## Error Handling

```python
try:
    response = client.ChatCompletion().create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
except Exception as e:
    print(f"Error: {e}")
    # Common errors:
    # - Invalid API key
    # - Insufficient credits
    # - Model not available
    # - Rate limit exceeded
```

## Best Practices

1. **Check Credits**: Always monitor your credit balance
2. **Use Appropriate Models**: Use smaller models for simple tasks
3. **Handle Errors**: Implement proper error handling
4. **Monitor Usage**: Track your usage patterns
5. **Cache Responses**: Cache responses when possible

## Deployment

### Self-Hosted

1. Clone the repository
2. Install dependencies: `pip install -r requirements_phase2.txt`
3. Set up environment variables (see `env_example.txt`)
4. Start the server: `python main_phase2.py`
5. Access dashboard: `http://localhost:8501`

### Cloud Deployment

Deploy to any cloud platform (AWS, GCP, Azure, Heroku, etc.):

```bash
# Example for Heroku
git push heroku main

# Example for Docker
docker build -t unillm .
docker run -p 8000:8000 unillm
```

## Support

- **Documentation**: Check the README files
- **Issues**: Report bugs in the repository
- **Community**: Join our Discord/community

## Pricing

UniLLM charges based on the actual cost of the underlying providers plus a small markup for the service. You can see real-time costs in your dashboard.

---

**Ready to get started?** Copy your API key from the dashboard and try the examples above! 