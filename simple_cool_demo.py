#!/usr/bin/env python3
"""
UniLLM SDK - Simple Cool Demo
=============================

A simple but powerful demo showing what you can build with UniLLM SDK:
- Multi-model chat
- Creative content generation
- Code improvement
- Model comparison
"""

import unillm
import time

# Your UniLLM credentials
API_KEY = "unillm_hSsZq5Yb9j9ph2g40Gb3Qx2pGIkfcBJz"
BASE_URL = "https://web-production-70deb.up.railway.app"

# Initialize the client
client = unillm.UniLLM(
    api_key=API_KEY,
    base_url=BASE_URL
)

def chat_with_model(message, model="gpt-3.5-turbo"):
    """Simple function to chat with any model"""
    try:
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
            max_tokens=500
        )
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

def demo_1_model_comparison():
    """Compare how different models answer the same question"""
    print("🤖 Demo 1: Model Comparison")
    print("=" * 50)
    
    question = "Write a haiku about artificial intelligence"
    
    models = ["gpt-3.5-turbo", "gpt-4", "claude-3-opus-20240229"]
    
    for model in models:
        print(f"\n📝 {model}:")
        print("-" * 30)
        response = chat_with_model(question, model)
        print(response)
        time.sleep(1)  # Be nice to the API

def demo_2_creative_writing():
    """Use different models for different creative tasks"""
    print("\n🎨 Demo 2: Creative Writing Pipeline")
    print("=" * 50)
    
    # Step 1: Generate a story idea with GPT-4
    print("📖 Step 1: Generating story idea with GPT-4...")
    idea = chat_with_model(
        "Give me a unique story idea about a robot learning to paint",
        "gpt-4"
    )
    print(idea)
    
    # Step 2: Develop characters with Claude
    print("\n👥 Step 2: Creating characters with Claude...")
    characters = chat_with_model(
        f"Based on this idea: {idea[:100]}...\n\nCreate 2 main characters for this story.",
        "claude-3-opus-20240229"
    )
    print(characters)
    
    # Step 3: Write opening scene with GPT-3.5
    print("\n🎬 Step 3: Writing opening scene with GPT-3.5...")
    scene = chat_with_model(
        "Write the opening paragraph of this robot painting story",
        "gpt-3.5-turbo"
    )
    print(scene)

def demo_3_code_improvement():
    """Improve code using different models"""
    print("\n💻 Demo 3: Code Improvement")
    print("=" * 50)
    
    # Sample inefficient code
    code = '''
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates
    '''
    
    print("🔍 Original code:")
    print(code)
    
    # Analyze with GPT-4
    print("\n📊 Analysis with GPT-4:")
    analysis = chat_with_model(
        f"Analyze this Python function and explain its issues:\n{code}",
        "gpt-4"
    )
    print(analysis)
    
    # Improve with Claude
    print("\n⚡ Improved version with Claude:")
    improved = chat_with_model(
        f"Rewrite this function to be more efficient:\n{code}",
        "claude-3-opus-20240229"
    )
    print(improved)

def demo_4_interactive_chat():
    """Interactive chat where you can switch models"""
    print("\n💬 Demo 4: Interactive Multi-Model Chat")
    print("=" * 50)
    print("Commands:")
    print("- Type your message to chat")
    print("- Type 'switch <model>' to change models")
    print("- Type 'quit' to exit")
    print("\nAvailable models: gpt-3.5-turbo, gpt-4, claude-3-opus-20240229")
    
    current_model = "gpt-3.5-turbo"
    
    while True:
        user_input = input(f"\n[{current_model}] You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower().startswith('switch '):
            new_model = user_input[7:].strip()
            if new_model in ["gpt-3.5-turbo", "gpt-4", "claude-3-opus-20240229"]:
                current_model = new_model
                print(f"✅ Switched to {current_model}")
            else:
                print("❌ Invalid model. Available: gpt-3.5-turbo, gpt-4, claude-3-opus-20240229")
        else:
            print(f"\n🤖 {current_model}:")
            response = chat_with_model(user_input, current_model)
            print(response)

def main():
    print("🚀 UniLLM SDK - Cool Demo")
    print("=" * 60)
    print("This demo shows the power of unified LLM access!")
    print("You can switch between OpenAI and Anthropic models seamlessly.")
    
    # Run all demos
    demo_1_model_comparison()
    demo_2_creative_writing()
    demo_3_code_improvement()
    
    # Ask if user wants interactive chat
    choice = input("\n🤔 Want to try interactive chat? (y/n): ").lower()
    if choice == 'y':
        demo_4_interactive_chat()
    
    print("\n🎉 Demo completed! Thanks for trying UniLLM SDK!")

if __name__ == "__main__":
    main() 