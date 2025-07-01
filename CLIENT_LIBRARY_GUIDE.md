# UniLLM Client Library Guide

This guide explains how to use the UniLLM client library to interact with your UniLLM API gateway.

## 📦 Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install unillm
```

### Option 2: Install from Source
```bash
git clone https://github.com/yourusername/unillm
cd unillm
pip install -e .
```

### Option 3: Use Without Installation
```bash
# Add the src directory to your Python path
export PYTHONPATH="/path/to/unillm/src:$PYTHONPATH"
```

## 🔑 Setup

### 1. Get Your API Key
1. Deploy your UniLLM API gateway (see deployment guide)
2. Register at the dashboard
3. Get your API key from the dashboard

### 2. Configure the Client
```python
# Method 1: Environment variable (recommended)
export UNILLM_API_KEY="your-api-key-here"

# Method 2: Pass directly to client
client = UniLLM(api_key="your-api-key-here")
```

## 🚀 Basic Usage

### Simple Chat
```python
from unillm import chat

response = chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content)
```

### Using the Client Class
```python
from unillm import UniLLM

client = UniLLM(api_key="your-api-key")

response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's 2+2?"}],
    temperature=0.7
)
print(response.content)
```

## 💬 Conversation Examples

### Basic Conversation
```python
messages = [
    {"role": "user", "content": "My name is Alice."},
    {"role": "assistant", "content": "Hello Alice! Nice to meet you."},
    {"role": "user", "content": "What's my name?"}
]

response = client.chat(model="gpt-4", messages=messages)
print(response.content)  # "Your name is Alice!"
```

### System Message
```python
messages = [
    {"role": "system", "content": "You are a helpful math tutor."},
    {"role": "user", "content": "What's the area of a circle with radius 5?"}
]

response = client.chat(model="gpt-4", messages=messages)
print(response.content)
```

### Multi-turn Conversation
```python
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "I'm learning Python."},
    {"role": "assistant", "content": "Great! Python is an excellent language to learn. What would you like to know?"},
    {"role": "user", "content": "How do I create a list?"},
    {"role": "assistant", "content": "You can create a list using square brackets: my_list = [1, 2, 3]"},
    {"role": "user", "content": "How do I add an item to that list?"}
]

response = client.chat(model="gpt-4", messages=conversation)
print(response.content)
```

## 🔧 Advanced Usage

### Custom Base URL
```python
client = UniLLM(
    api_key="your-api-key",
    base_url="https://your-deployed-api.com"
)
```

### Parameters
```python
response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a short story"}],
    temperature=0.8,      # Creativity (0-2)
    max_tokens=500,       # Maximum response length
    top_p=0.9,           # Nucleus sampling
    frequency_penalty=0.1, # Reduce repetition
    presence_penalty=0.1   # Encourage new topics
)
```

### Health Check
```python
if client.health_check():
    print("✅ API is healthy!")
else:
    print("❌ API is not responding")
```

## 📊 Response Object

The `ChatResponse` object contains:

```python
response = client.chat(model="gpt-4", messages=[{"role": "user", "content": "Hello"}])

print(response.content)      # The generated text
print(response.model)        # Model used (e.g., "gpt-4")
print(response.usage)        # Token usage info
print(response.finish_reason) # Why it stopped ("stop", "length", etc.)

# Convert to string
print(str(response))         # Same as response.content
```

## 🎯 Supported Models

UniLLM automatically routes to the correct provider:

| Provider | Models | Example |
|----------|--------|---------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-3.5-turbo | `"gpt-4"` |
| Anthropic | claude-3-sonnet, claude-3-haiku | `"claude-3-sonnet"` |
| Google | gemini-pro, gemini-pro-vision | `"gemini-pro"` |
| Mistral | mistral-large, mistral-medium | `"mistral-large"` |
| Cohere | command, command-light | `"command"` |

## ⚠️ Error Handling

```python
from unillm import UniLLM, UniLLMError

try:
    response = client.chat(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.content)
    
except UniLLMError as e:
    print(f"UniLLM error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🧪 Testing

Test your setup:
```bash
# Test the client library
python test_client_library.py

# Or run the example
python examples/simple_client_example.py
```

## 🔄 Migration from OpenAI

If you're migrating from the OpenAI library:

```python
# Before (OpenAI)
import openai
openai.api_key = "your-openai-key"
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)

# After (UniLLM)
from unillm import UniLLM
client = UniLLM(api_key="your-unillm-key")
response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.content)
```

## 📈 Usage Tracking

All requests are automatically tracked:
- Token usage (prompt, completion, total)
- Cost per model
- Request history
- Analytics in the dashboard

## 🚀 Next Steps

1. **Deploy your API gateway** (see deployment guide)
2. **Test with the examples** in the `examples/` directory
3. **Integrate into your application**
4. **Monitor usage** through the dashboard

## 🆘 Troubleshooting

### Common Issues

**"API key required"**
- Set `UNILLM_API_KEY` environment variable
- Or pass `api_key` parameter to `UniLLM()`

**"API is not responding"**
- Make sure your API gateway is running
- Check the base URL (default: localhost:8000)
- Verify network connectivity

**"Model not found"**
- Check the model name spelling
- Ensure the provider API key is configured
- See supported models list

**"Authentication failed"**
- Verify your UniLLM API key is correct
- Check if your account has credits
- Ensure the API key is active

### Getting Help

- Check the [main README](../README.md)
- Look at the [examples](../examples/) directory
- Open an issue on GitHub
- Check the API gateway logs for errors 