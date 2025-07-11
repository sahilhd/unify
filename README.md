# UniLLM - Unified API Gateway for Multiple LLM Providers

[![PyPI version](https://badge.fury.io/py/unifyllm-sdk.svg)](https://badge.fury.io/py/unifyllm-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A unified API gateway that provides a single API key interface for multiple LLM providers (OpenAI, Anthropic, Google, Mistral, Cohere) with built-in usage tracking, billing, and a modern web dashboard.

## 🎯 What is UniLLM?

UniLLM solves the complexity of managing multiple LLM API keys by providing:

- **🔑 Single API Key**: Use one key to access all supported providers
- **🤖 Automatic Provider Selection**: Smart routing based on model names
- **📊 Usage Tracking**: Built-in analytics and cost monitoring
- **🎨 Modern Dashboard**: React-based web interface for management
- **💳 Credit System**: Pre-paid credits with automatic deduction
- **🔄 Drop-in Replacements**: Compatible with OpenAI and Anthropic libraries
- **⚡ Retry Logic**: Automatic handling of server overloads

---

# 🚀 Option 1: Use UniLLM as a Service (Recommended for Most Users)

**Get started in minutes with our managed UniLLM service. No setup required - just sign up and start using the unified API.**

## Quick Start (2 minutes)

### 1. Install the Client Library
```bash
pip install unifyllm-sdk
```

### 2. Get Your API Key
1. **Sign up** at [unillm.com](https://unillm.com) (or your deployed frontend URL)
2. **Get your API key** from the dashboard
3. **Set your API key**: `export UNILLM_API_KEY="your-api-key-here"`

### 3. Start Using UniLLM
```python
from unillm import UniLLM

# Just provide your API key - everything else is pre-configured!
client = UniLLM(api_key="your-api-key")

response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello! What's 2+2?"}]
)
print(response.content)  # "2+2 equals 4."
```

## 🎨 Dashboard Features

Access your modern React dashboard for:
- **User Management**: Register, login, manage API keys
- **Usage Analytics**: Real-time usage statistics and cost tracking
- **Billing**: Credit purchase and management with Stripe
- **Chat Interface**: Test models directly in the browser
- **API Keys**: Secure key management with copy/hide functionality

## 💳 Pricing & Credits

- **Pay-as-you-go**: Purchase credits and use them across all models
- **No monthly fees**: Only pay for what you use
- **Transparent pricing**: See exact costs per model
- **Bulk discounts**: Save more with larger credit packages

**Starting at $5 for thousands of GPT-3.5 calls**

## 🔄 Drop-in Replacements

### OpenAI Compatibility
```python
from unillm import openai

# Configure
openai.api_key = "your-unillm-api-key"
# No need to set api_base - it's pre-configured for SaaS!

# Use exactly like OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=50
)
print(response.choices[0].message.content)
```

### Anthropic Compatibility
```python
from unillm import anthropic

# Configure
anthropic.api_key = "your-unillm-api-key"
# No need to set api_base - it's pre-configured for SaaS!

# Use exactly like Anthropic
response = anthropic.messages.create(
    model="claude-3-sonnet",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=50
)
print(response.content[0].text)
```

## 📋 Supported Models

UniLLM automatically routes to the correct provider based on the model name:

### 🤖 OpenAI Models
- `gpt-4` - Most capable model
- `gpt-4-turbo` - Latest GPT-4 with improved performance
- `gpt-4o` - Latest OpenAI model
- `gpt-4o-mini` - Faster, more efficient model
- `gpt-3.5-turbo` - Fast and cost-effective

### 🧠 Anthropic Models
- `claude-3-opus` - Most capable Claude model
- `claude-3-sonnet` - Balanced performance and speed
- `claude-3-haiku` - Fastest and most cost-effective
- `claude-3-5-sonnet-20241022` - Latest Sonnet model
- `claude-3-5-haiku-20241022` - Latest Haiku model

### 🔍 Google Models
- `gemini-pro` - Google's most capable model
- `gemini-pro-vision` - Vision-enabled model
- `gemini-1.5-pro` - Latest Gemini Pro
- `gemini-1.5-flash` - Fast Gemini model

### 🌪️ Mistral Models
- `mistral-large` - Most capable Mistral model
- `mistral-medium` - Balanced performance
- `mistral-small` - Fast and efficient

### 🎯 Cohere Models
- `command` - Cohere's flagship model
- `command-light` - Faster, lighter model

## 🔧 Configuration

### Environment Variables
```bash
export UNILLM_API_KEY="your-api-key"
# No need to set UNILLM_BASE_URL for SaaS - it's pre-configured!
```

### Client Configuration
```python
# For SaaS users - just provide your API key
client = UniLLM(api_key="your-api-key")

# The library automatically connects to our managed service
```

## 📊 Advanced Features

### Health Check
```python
# Check if the API gateway is healthy
is_healthy = client.health_check()
print(f"API Gateway healthy: {is_healthy}")
```

### Provider Switching
```python
# Switch between providers seamlessly
providers = [
    ("gpt-4", "OpenAI"),
    ("claude-3-sonnet", "Anthropic"),
    ("gemini-pro", "Google"),
    ("mistral-large", "Mistral")
]

for model, provider in providers:
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": "Say hello from your provider!"}],
        max_tokens=30
    )
    print(f"{provider}: {response.content}")
```

### Advanced Parameters
```python
response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Generate a creative story."}],
    temperature=0.8,      # Creativity (0.0-2.0)
    max_tokens=200,       # Maximum response length
    top_p=0.9,           # Nucleus sampling
    frequency_penalty=0.1, # Reduce repetition
    presence_penalty=0.1   # Encourage new topics
)
```

---

# 🏠 Option 2: Self-Host UniLLM (For Companies & Teams)

**Deploy UniLLM on your own infrastructure for full privacy, compliance, and customization. Perfect for enterprises and teams with special requirements.**

## Why Self-Host?

- **🔒 Privacy**: Your data never leaves your infrastructure
- **💰 Cost Control**: No markup on API calls, pay only what providers charge
- **⚡ Performance**: Lower latency, no shared infrastructure
- **🔧 Customization**: Modify the code to fit your specific needs
- **📊 Full Analytics**: Complete control over usage tracking and billing

## Quick Self-Hosting (5 minutes)

```bash
# Clone and setup
git clone https://github.com/yourusername/unillm
cd unillm
./quick_start.sh

# Or manually:
cd api_gateway
pip install -r requirements.txt
cp env_example.txt .env
# Edit .env with your API keys
python main_phase2.py
```

## Production Deployment

### Docker (Recommended)
```bash
# Create .env file with your API keys
cp env_example.txt .env
# Edit .env

# Deploy with Docker Compose
docker-compose up -d
```

### VPS Deployment
Complete guide for deploying on your own server with nginx, SSL, and PostgreSQL.

## Test Your Setup
```bash
# Verify your self-hosted instance
python test_self_hosted.py

# Or test a specific URL
python test_self_hosted.py https://your-domain.com
```

## 🔧 Self-Hosting Configuration

When self-hosting, you need to specify your own server URL:

### Environment Variables
```bash
export UNILLM_API_KEY="your-api-key"
export UNILLM_BASE_URL="https://your-self-hosted-domain.com"  # Your server URL
```

### Client Configuration
```python
client = UniLLM(
    api_key="your-api-key",
    base_url="https://your-self-hosted-domain.com"  # Your server URL
)
```

### OpenAI/Anthropic Compatibility
```python
from unillm import openai

openai.api_key = "your-api-key"
openai.api_base = "https://your-self-hosted-domain.com"  # Your server URL
```

📖 **Complete self-hosting guide**: [SELF_HOSTING_GUIDE.md](SELF_HOSTING_GUIDE.md)

---

## 📚 Complete Examples

### Example 1: Multi-Provider Chat Bot
```python
from unillm import UniLLM

client = UniLLM(api_key="your-api-key")

def chat_with_provider(provider, message):
    models = {
        "OpenAI": "gpt-4",
        "Anthropic": "claude-3-sonnet", 
        "Google": "gemini-pro",
        "Mistral": "mistral-large"
    }
    
    response = client.chat(
        model=models[provider],
        messages=[{"role": "user", "content": message}],
        max_tokens=100
    )
    return response.content

# Test all providers
question = "What is the capital of France?"
for provider in ["OpenAI", "Anthropic", "Google", "Mistral"]:
    answer = chat_with_provider(provider, question)
    print(f"{provider}: {answer}")
```

### Example 2: Conversation Memory
```python
class ConversationBot:
    def __init__(self, api_key):
        self.client = UniLLM(api_key=api_key)
        self.conversation = []
    
    def add_message(self, role, content):
        self.conversation.append({"role": role, "content": content})
    
    def get_response(self, user_message, model="gpt-4"):
        self.add_message("user", user_message)
        
        response = self.client.chat(
            model=model,
            messages=self.conversation,
            max_tokens=150
        )
        
        self.add_message("assistant", response.content)
        return response.content

# Usage
bot = ConversationBot("your-api-key")
bot.add_message("system", "You are a helpful assistant.")

print(bot.get_response("My name is John."))
print(bot.get_response("What's my name?"))  # Remembers the conversation
```

### Example 3: Error Handling
```python
from unillm import UniLLM, UniLLMError

client = UniLLM(api_key="your-api-key")

try:
    response = client.chat(
        model="invalid-model",
        messages=[{"role": "user", "content": "Hello"}]
    )
except UniLLMError as e:
    print(f"Error: {e}")
    # Try with a valid model
    response = client.chat(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(f"Success: {response.content}")
```

## 🧪 Testing

Test your setup with our comprehensive test suite:

```bash
# Set your API key
export UNILLM_API_KEY="your-api-key"

# Run comprehensive tests
python test_comprehensive.py
```

This will test:
- ✅ Basic chat functionality
- ✅ Multi-provider support
- ✅ Drop-in replacements
- ✅ Error handling
- ✅ Retry logic
- ✅ Environment variables
- ✅ Advanced features

## 📊 Usage Tracking

The client automatically tracks usage through your API gateway:
- **Token usage** (prompt, completion, total)
- **Cost tracking** per model
- **Request history**
- **Analytics dashboard**

## 🔧 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'fastapi'"**
   - Install backend dependencies: `pip install -r requirements.txt`

2. **"Invalid API key"**
   - Check your API key is correct
   - Ensure you have credits in your account

3. **"Model not available"**
   - Check the supported models list
   - Ensure the model name is correct

4. **"Server overloaded"**
   - The retry logic will handle this automatically
   - Wait a few moments and try again

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/unillm/issues)
- **Documentation**: [GitHub Wiki](https://github.com/yourusername/unillm/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/unillm/discussions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests: `python test_comprehensive.py`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend with [React](https://reactjs.org/)
- Inspired by the need for unified LLM access

---

**Ready to get started?** Choose your option above and try the [quick start examples](#quick-start-2-minutes)! 