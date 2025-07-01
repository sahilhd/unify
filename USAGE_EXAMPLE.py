# UniLLM Client Library Usage Example

# 1. Install the library
# pip install unillm-0.1.0-py3-none-any.whl

# 2. Import and use
from unillm.client import UniLLM

# Create client (point to your deployed API)
client = UniLLM(
    api_key="your_api_key_here",  # Get this from the dashboard
    base_url="https://your-deployed-api.com"  # Your Railway/Render URL
)

# Test OpenAI
response = client.chat(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello from OpenAI!"}]
)
print("OpenAI Response:", response.content)

# Test Anthropic
response = client.chat(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Hello from Anthropic!"}]
)
print("Anthropic Response:", response.content)

# Health check
if client.health_check():
    print("✅ API is healthy!")
else:
    print("❌ API is not responding")
