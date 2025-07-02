# UniLLM SDK - Cool Demo

This demo showcases the power of the **UniLLM SDK** - a unified Python library that lets you access multiple LLM providers (OpenAI, Anthropic, etc.) with a single API key!

## 🚀 What This Demo Shows

### 1. **Model Comparison** 🤖
Compare how different AI models answer the same question:
- **GPT-3.5 Turbo**: Fast and efficient
- **GPT-4**: Most capable for complex reasoning  
- **Claude-3 Opus**: Creative and analytical

### 2. **Creative Writing Pipeline** 🎨
Use different models for different creative tasks:
- **GPT-4**: Generate story concepts
- **Claude**: Develop characters
- **GPT-3.5**: Write scenes

### 3. **Code Improvement** 💻
Get code analysis and improvements from different models:
- **GPT-4**: Detailed code analysis
- **Claude**: Optimized code generation

### 4. **Interactive Multi-Model Chat** 💬
Chat interactively and switch between models on the fly!

## 🛠️ How to Run

### Prerequisites
```bash
pip install unifyllm-sdk
```

### Run the Demo
```bash
python3 simple_cool_demo.py
```

## 📝 What You Can Build

With UniLLM SDK, you can build:

- **Multi-model AI assistants** that switch between providers
- **Creative writing tools** that use the best model for each task
- **Code review systems** that get feedback from multiple AI models
- **Content generation pipelines** that leverage different model strengths
- **AI comparison tools** to see how different models perform
- **Fallback systems** that automatically switch models if one fails

## 🔑 Key Benefits

1. **Single API Key**: Access multiple providers with one key
2. **Seamless Switching**: Change models without changing code
3. **Unified Interface**: Same API for all providers
4. **Cost Optimization**: Use the most cost-effective model for each task
5. **Reliability**: Automatic fallback if one provider is down

## 🌟 Example Usage

```python
import unillm

# Initialize with your API key
client = unillm.UniLLM(
    api_key="your_api_key_here",
    base_url="https://web-production-70deb.up.railway.app"
)

# Chat with any model
response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content)
```

## 🎯 Get Your API Key

1. Visit: https://web-production-70deb.up.railway.app
2. Register for an account
3. Get your API key
4. Start building cool AI applications!

---

**Built with ❤️ using UniLLM SDK** 