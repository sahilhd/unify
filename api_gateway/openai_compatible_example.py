"""
UniLLM OpenAI-Compatible Example
This shows how to use UniLLM exactly like the OpenAI library.
"""

# Import our UniLLM client (works like OpenAI)
from unillm_client_library import UniLLMClient

# Set your UniLLM API key (get this from your dashboard)
API_KEY = "your_unillm_api_key_here"  # Replace with your actual API key

# Initialize the client (just like OpenAI)
client = UniLLMClient(API_KEY)

print("🤖 UniLLM OpenAI-Compatible Example")
print("=" * 50)

# Example 1: Use GPT-4o (OpenAI)
print("\n1️⃣ Testing GPT-4o (OpenAI):")
response = client.ChatCompletion().create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's the difference between machine learning and deep learning?"}
    ],
    max_tokens=150,
    temperature=0.7
)

print(f"Response: {response.choices[0].message.content}")
print(f"Provider: {response.provider}")
print(f"Cost: ${response.cost:.6f}")
print(f"Remaining credits: {response.remaining_credits}")

# Example 2: Switch to Claude-3-sonnet (Anthropic) - SAME API!
print("\n2️⃣ Testing Claude-3-sonnet (Anthropic):")
response2 = client.ChatCompletion().create(
    model="claude-3-sonnet",
    messages=[
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ],
    max_tokens=100,
    temperature=0.5
)

print(f"Response: {response2.choices[0].message.content}")
print(f"Provider: {response2.provider}")
print(f"Cost: ${response2.cost:.6f}")
print(f"Remaining credits: {response2.remaining_credits}")

# Example 3: Switch to Gemini Pro (Google) - SAME API!
print("\n3️⃣ Testing Gemini Pro (Google):")
response3 = client.ChatCompletion().create(
    model="gemini-pro",
    messages=[
        {"role": "user", "content": "Write a short poem about AI"}
    ],
    max_tokens=80,
    temperature=0.8
)

print(f"Response: {response3.choices[0].message.content}")
print(f"Provider: {response3.provider}")
print(f"Cost: ${response3.cost:.6f}")
print(f"Remaining credits: {response3.remaining_credits}")

# Example 4: Get usage statistics
print("\n4️⃣ Usage Statistics:")
usage = client.get_usage_stats()
print(f"Total requests: {usage.get('total_requests', 0)}")
print(f"Total tokens: {usage.get('total_tokens', 0)}")
print(f"Total cost: ${usage.get('total_cost', 0):.6f}")

print("\n🎉 That's it! You can switch between any LLM provider with the same API!")
print("📚 Available models: gpt-4o, gpt-3.5-turbo, claude-3-sonnet, claude-3-haiku, gemini-pro, etc.") 